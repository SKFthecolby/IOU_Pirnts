from __future__ import annotations
import csv
from pathlib import Path

def _write(path: Path, rows, headers):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(headers); w.writerows(rows)

def generate_reports(conn, outdir: Path):
    _write(outdir/'full_inventory.csv', conn.execute('SELECT * FROM files').fetchall(), [c[1] for c in conn.execute('PRAGMA table_info(files)')])
    _write(outdir/'folders_inventory.csv', conn.execute('SELECT * FROM folders').fetchall(), [c[1] for c in conn.execute('PRAGMA table_info(folders)')])
    _write(outdir/'detected_projects.csv', conn.execute('SELECT * FROM projects').fetchall(), [c[1] for c in conn.execute('PRAGMA table_info(projects)')])
