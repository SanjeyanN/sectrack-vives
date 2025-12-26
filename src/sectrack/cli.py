from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # .../sectrack/ (project root)

from sectrack.config import load_config
from sectrack.db import Database
from sectrack.models import Host
from sectrack.export import export_rows_to_csv


def cmd_init_db(db: Database) -> int:
    db.init_schema()
    print("OK: database schema initialized.")
    return 0


def cmd_add_host(db: Database) -> int:
    print("Add host (leave blank to skip optional fields)")
    hostname = input("Hostname*: ").strip()
    if not hostname:
        print("Error: hostname is required.")
        return 1

    ip = input("IP: ").strip() or None
    owner = input("Owner: ").strip() or None
    notes = input("Notes: ").strip() or None

    # class object instantiation (requirement)
    host = Host(hostname=hostname, ip=ip, owner=owner, notes=notes)

    db.execute(
        "INSERT INTO hosts(hostname, ip, owner, notes) VALUES (?, ?, ?, ?)",
        (host.hostname, host.ip, host.owner, host.notes),
    )
    print("OK: host added.")
    return 0


def cmd_list_hosts(db: Database) -> int:
    rows = db.query("SELECT id, hostname, ip, owner, notes FROM hosts ORDER BY id DESC")
    if not rows:
        print("No hosts found.")
        return 0

    for r in rows:
        print(f"[{r['id']}] {r['hostname']}  ip={r['ip'] or '-'}  owner={r['owner'] or '-'}")
    return 0


def cmd_search_host(db: Database, term: str) -> int:
    term_like = f"%{term}%"
    rows = db.query(
        """
        SELECT id, hostname, ip, owner, notes
        FROM hosts
        WHERE hostname LIKE ? OR ip LIKE ? OR owner LIKE ? OR notes LIKE ?
        ORDER BY id DESC
        """,
        (term_like, term_like, term_like, term_like),
    )
    if not rows:
        print("No matches.")
        return 0

    for r in rows:
        print(f"[{r['id']}] {r['hostname']}  ip={r['ip'] or '-'}  owner={r['owner'] or '-'}")
    return 0

def cmd_add_finding(db: Database) -> int:
    print("Add finding")
    host_id = input("Host ID*: ").strip()
    if not host_id.isdigit():
        print("Invalid host ID")
        return 1

    title = input("Title*: ").strip()
    severity = input("Severity (low/medium/high/critical)*: ").strip().lower()
    if severity not in ("low", "medium", "high", "critical"):
        print("Invalid severity")
        return 1

    status = input("Status (open/fixed/wontfix) [open]: ").strip() or "open"

    db.execute(
        """
        INSERT INTO findings(host_id, title, severity, status, created_at)
        VALUES (?, ?, ?, ?, date('now'))
        """,
        (int(host_id), title, severity, status),
    )

    print("OK: finding added.")
    return 0

def cmd_export_hosts_csv(db: Database, export_dir: Path) -> int:
    rows = db.query("SELECT id, hostname, ip, owner, notes FROM hosts ORDER BY id ASC")
    out_path = export_dir / "hosts.csv"
    export_rows_to_csv((dict(r) for r in rows), out_path)
    print(f"OK: exported to {out_path}")
    return 0

def cmd_list_findings(db: Database) -> int:
    rows = db.query(
        """
        SELECT f.id, h.hostname, f.title, f.severity, f.status, f.created_at
        FROM findings f
        JOIN hosts h ON f.host_id = h.id
        ORDER BY f.id DESC
        """
    )

    if not rows:
        print("No findings found.")
        return 0

    for r in rows:
        print(
            f"[{r['id']}] {r['hostname']} | {r['title']} | "
            f"{r['severity']} | {r['status']} | {r['created_at']}"
        )
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="sectrack", description="SecTrack CLI (SQLite)")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init-db", help="Create tables if missing")
    sub.add_parser("add-host", help="Add a host")
    sub.add_parser("list-hosts", help="List hosts")
    sub.add_parser("add-finding", help="Add a finding to a host")
    sub.add_parser("list-findings", help="List findings")

    sp = sub.add_parser("search-host", help="Search hosts by term")
    sp.add_argument("term")

    exp = sub.add_parser("export-hosts", help="Export hosts")
    exp.add_argument("--csv", action="store_true", help="Export to data/exports/hosts.csv")

    return p


def main() -> int:
    args = build_parser().parse_args()
    cfg = load_config(str(ROOT / "settings.ini"))
    db = Database(cfg.db_path)

    if args.cmd == "init-db":
        return cmd_init_db(db)
    if args.cmd == "add-host":
        return cmd_add_host(db)
    if args.cmd == "add-finding":
        return cmd_add_finding(db)
    if args.cmd == "list-hosts":
        return cmd_list_hosts(db)
    if args.cmd == "list-findings":
        return cmd_list_findings(db)
    if args.cmd == "search-host":
        return cmd_search_host(db, args.term)
    if args.cmd == "export-hosts":
        if args.csv:
            return cmd_export_hosts_csv(db, cfg.export_dir)
        print("Nothing to do. Use --csv.")
        return 2

    print("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())


