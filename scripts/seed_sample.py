import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sectrack.config import load_config
from sectrack.db import Database


def main() -> int:
    cfg = load_config(str(ROOT / "settings.ini"))
    db = Database(cfg.db_path)
    db.init_schema()

    # Clear existing data (repeatable)
    db.execute("DELETE FROM findings")
    db.execute("DELETE FROM hosts")

    # Insert sample hosts
    hosts = [
        ("webserver01", "192.168.1.10", "home-lab", "nginx, exposed to LAN"),
        ("nas01", "192.168.1.20", "storage", "SMB enabled, check guest access"),
        ("router", "192.168.1.1", "network", "admin panel, firmware version?"),
    ]
    for h in hosts:
        db.execute("INSERT INTO hosts(hostname, ip, owner, notes) VALUES (?, ?, ?, ?)", h)

    # Map hostname -> id
    rows = db.query("SELECT id, hostname FROM hosts")
    ids = {r["hostname"]: r["id"] for r in rows}

    # Insert sample findings
    findings = [
        (ids["webserver01"], "Open SSH port (22) to LAN", "medium", "open"),
        (ids["webserver01"], "Outdated nginx version", "high", "open"),
        (ids["nas01"], "SMB guest access enabled", "critical", "open"),
        (ids["router"], "Default admin username suspected", "high", "wontfix"),
    ]
    for f in findings:
        db.execute(
            """
            INSERT INTO findings(host_id, title, severity, status, created_at)
            VALUES (?, ?, ?, ?, date('now'))
            """,
            f,
        )

    print(f"OK: seeded sample data into {cfg.db_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
