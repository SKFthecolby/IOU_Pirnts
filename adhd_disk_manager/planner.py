from __future__ import annotations
from pathlib import Path
from datetime import datetime
import csv
from safe_paths import safe_destination


def build_plan(conn, rules: dict, report_dir: Path):
    batch_id = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    dst_root = Path(rules['destination_root'])
    report_dir.mkdir(parents=True, exist_ok=True)
    plan=[]; conflicts=[]; skipped=[]
    files = conn.execute('SELECT full_path,filename,extension,category,protected_root,size_bytes FROM files').fetchall()
    for r in files:
        src = Path(r['full_path'])
        if r['protected_root']:
            skipped.append([src,'protected_internal'])
            continue
        rel = rules.get('category_destinations',{}).get(r['category'],'99_UNKNOWN_REVIEW')
        ext_map = rules.get('extension_rules',{})
        if r['extension'] in ext_map:
            rel = ext_map[r['extension']]
        dest = safe_destination(dst_root, rel) / src.name
        conflict = dest.exists()
        plan.append([batch_id,'move','file',str(src),str(dest),r['category'],'category_or_ext','not_protected','conflict' if conflict else 'none',1,'' if not conflict else 'destination exists'])
        if conflict: conflicts.append([src,dest,'exists'])
    with (report_dir/'move_plan.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['batch_id','action','item_type','source_path','destination_path','category','matched_rule','protected_status','conflict_status','approved','warning']); w.writerows(plan)
    with (report_dir/'conflicts.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['source','destination','reason']); w.writerows(conflicts)
    with (report_dir/'protected_skipped.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['path','reason']); w.writerows(skipped)
    (report_dir/'move_plan.md').write_text(f'# Move Plan {batch_id}\n\nItems: {len(plan)}\nConflicts: {len(conflicts)}\nSkipped protected: {len(skipped)}\n', encoding='utf-8')
    return batch_id, len(plan), len(conflicts), len(skipped)
