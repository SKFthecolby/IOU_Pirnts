from __future__ import annotations
import argparse
from pathlib import Path
import sys
import yaml

if __package__ in (None, ''):
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from adhd_disk_manager.database import connect
from adhd_disk_manager.drive_discovery import list_windows_drives, select_roots
from adhd_disk_manager.scanner import scan_paths
from adhd_disk_manager.search import text_search, by_ext, by_category
from adhd_disk_manager.reports import generate_reports
from adhd_disk_manager.planner import build_plan
from adhd_disk_manager.mover import execute_move
from adhd_disk_manager.rollback import list_batches, run_rollback
from adhd_disk_manager.duplicate_detector import detect_duplicates
from adhd_disk_manager.tui import show_menu


def load_yaml(p: Path):
    return yaml.safe_load(p.read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser(description='Windows-friendly safe file inventory and organizer')
    parser.add_argument('--config', default='config.yaml', help='Path to config YAML')
    sub = parser.add_subparsers(dest='cmd', required=True)
    sub.add_parser('drives')
    sc = sub.add_parser('scan'); sc.add_argument('--all-drives', action='store_true'); sc.add_argument('--drive'); sc.add_argument('--root', action='append')
    se = sub.add_parser('search'); se.add_argument('term')
    ex = sub.add_parser('ext'); ex.add_argument('ext')
    ca = sub.add_parser('category'); ca.add_argument('category')
    sub.add_parser('projects'); sub.add_parser('duplicates'); sub.add_parser('report'); sub.add_parser('plan')
    mv = sub.add_parser('move'); mv.add_argument('--dry-run', action='store_true'); mv.add_argument('--yes-confirmation-string')
    rb = sub.add_parser('rollback'); rb.add_argument('--list', action='store_true'); rb.add_argument('--batch'); rb.add_argument('--execute', action='store_true')
    sub.add_parser('tui')
    a = parser.parse_args()

    cfg = load_yaml(Path(a.config))
    rules = load_yaml(Path(cfg['rules_path']))
    conn = connect(cfg['database_path'])
    reports_dir = Path(cfg['reports_dir']); rollback_dir = Path(cfg['rollback_dir'])

    if a.cmd == 'drives': print('\n'.join(list_windows_drives()))
    elif a.cmd == 'scan':
        roots = select_roots(a.all_drives, a.drive, a.root, rules.get('drive_scan', {}).get('excluded_drives', []))
        scan_cfg = cfg.get('scan', {})
        scan_paths(conn, roots, rules, batch_size=int(scan_cfg.get('batch_size', 250)), skip_hidden=bool(scan_cfg.get('skip_hidden', False)), follow_symlinks=bool(scan_cfg.get('follow_symlinks', False)))
        print(f'Scanned {len(roots)} roots')
    elif a.cmd == 'search': [print(r['full_path']) for r in text_search(conn, a.term)]
    elif a.cmd == 'ext': [print(r['full_path']) for r in by_ext(conn, a.ext)]
    elif a.cmd == 'category': [print(r['full_path']) for r in by_category(conn, a.category)]
    elif a.cmd == 'projects': [print(r['root_path']) for r in conn.execute('SELECT root_path FROM projects')]
    elif a.cmd == 'duplicates': print(f'Candidates: {len(detect_duplicates(conn))}')
    elif a.cmd == 'report': generate_reports(conn, reports_dir); print('Reports generated')
    elif a.cmd == 'plan':
        b, p, c, s = build_plan(conn, rules, reports_dir)
        print(f'Batch {b}: planned={p} conflicts={c} protected_skipped={s}')
    elif a.cmd == 'move':
        require_conf = bool(rules.get('mode', {}).get('require_confirmation', True))
        b, m, f = execute_move(conn, reports_dir, rollback_dir, a.dry_run, a.yes_confirmation_string, require_confirmation=require_conf)
        print(f'Batch {b}: moved={m} failed={f}')
    elif a.cmd == 'rollback':
        if a.list:
            for p in list_batches(rollback_dir): print(p.name)
        elif a.batch:
            manifest = rollback_dir / f'rollback_{a.batch}.json'
            total, restored = run_rollback(manifest, execute=a.execute)
            print(f'Rollback rows={total}, restored={restored}, execute={a.execute}')
    elif a.cmd == 'tui': show_menu()


if __name__ == '__main__':
    main()
