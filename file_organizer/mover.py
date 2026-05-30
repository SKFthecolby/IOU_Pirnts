from __future__ import annotations
from pathlib import Path
from datetime import datetime
import csv, json, shutil


def execute_move(conn, report_dir: Path, rollback_dir: Path, dry_run: bool, confirm: str | None, require_confirmation: bool = True):
    plan_path = report_dir / 'move_plan.csv'
    rows = list(csv.DictReader(plan_path.open(encoding='utf-8')))
    if not rows:
        raise RuntimeError('No plan rows')
    batch_id = rows[0]['batch_id']
    required = f'MOVE BATCH {batch_id}'
    if not dry_run and require_confirmation and confirm != required:
        raise RuntimeError(f'Confirmation mismatch. Required: {required}')

    rollback_dir.mkdir(exist_ok=True)
    manifest = []
    moved = 0
    failed = 0

    for r in rows:
        if str(r.get('approved', '1')).strip() not in {'1', 'true', 'True', 'yes', 'YES'}:
            continue
        src = Path(r['source_path'])
        dst = Path(r['destination_path'])
        status = 'dry_run' if dry_run else 'pending'
        err = ''
        try:
            if r['conflict_status'] != 'none':
                status = 'skipped_conflict'
            elif not dry_run:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dst))
                status = 'moved'
                moved += 1
            manifest.append({'batch_id': batch_id, 'move_time': datetime.utcnow().isoformat(), 'source_original': str(src), 'destination_moved': str(dst), 'item_type': r['item_type'], 'size_bytes': 0, 'sha256_before_optional': '', 'sha256_after_optional': '', 'move_status': status, 'rollback_status': '', 'error': err})
        except Exception as e:
            failed += 1
            manifest.append({'batch_id': batch_id, 'move_time': datetime.utcnow().isoformat(), 'source_original': str(src), 'destination_moved': str(dst), 'item_type': r['item_type'], 'size_bytes': 0, 'sha256_before_optional': '', 'sha256_after_optional': '', 'move_status': 'failed', 'rollback_status': '', 'error': str(e)})

    if not manifest:
        raise RuntimeError('No approved rows to execute from move_plan.csv')

    mjson = rollback_dir / f'rollback_{batch_id}.json'
    mjson.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    with (rollback_dir / f'rollback_{batch_id}.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(manifest[0].keys()))
        w.writeheader()
        w.writerows(manifest)
    conn.execute(
        'INSERT OR REPLACE INTO move_batches(batch_id,created_time,executed_time,status,total_items,moved_items,failed_items,total_size_bytes,rollback_manifest) VALUES (?,?,?,?,?,?,?,?,?)',
        (
            batch_id,
            datetime.utcnow().isoformat(),
            datetime.utcnow().isoformat(),
            'dry_run' if dry_run else 'executed',
            len(manifest),
            moved,
            failed,
            0,
            str(mjson),
        ),
    )
    conn.commit()
    return batch_id, moved, failed
