from __future__ import annotations
from openpyxl import Workbook
import csv
from pathlib import Path
from typing import Iterable, Mapping, Any

def export_rows_to_csv(rows: Iterable[Mapping[str, Any]], out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    rows = list(rows)

    if not rows:
        out_path.write_text("", encoding="utf-8")
        return out_path

    fieldnames = list(rows[0].keys())
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(dict(r))
    return out_path

def export_rows_to_excel(rows, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    wb = Workbook()
    ws = wb.active
    ws.title = "Findings"

    rows = list(rows)
    if not rows:
        wb.save(out_path)
        return out_path

    ws.append(list(rows[0].keys()))
    for r in rows:
        ws.append(list(r.values()))

    wb.save(out_path)
    return out_path

