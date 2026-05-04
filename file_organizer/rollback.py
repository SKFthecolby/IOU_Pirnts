from __future__ import annotations
from pathlib import Path
import json, shutil

def list_batches(rollback_dir: Path):
    return sorted(rollback_dir.glob('rollback_*.json'))

def run_rollback(manifest: Path, execute: bool=False):
    rows = json.loads(manifest.read_text(encoding='utf-8'))
    restored=0
    for r in rows:
        src = Path(r['destination_moved']); dst = Path(r['source_original'])
        if not execute:
            continue
        if dst.exists():
            raise RuntimeError(f'Conflict on rollback: {dst}')
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.exists():
            shutil.move(str(src), str(dst)); restored += 1
    return len(rows), restored
