from __future__ import annotations
from pathlib import Path
from datetime import datetime
import os
from classifier import classify
from project_detector import detect_project_root


def scan_paths(conn, roots: list[Path], rules: dict, logger=print, batch_size: int = 250):
    markers = rules.get('protected_markers', [])
    excluded = rules.get('never_move_paths_contains', [])
    scan_time = datetime.utcnow().isoformat()
    files_batch=[]
    folders_batch=[]
    projects=set()
    for root in roots:
        for dirpath, dirnames, filenames in os.walk(root, topdown=True):
            p = Path(dirpath)
            if any(t.lower() in str(p).lower() for t in excluded):
                dirnames[:] = []
                continue
            is_project, found = detect_project_root(p, markers)
            if is_project:
                projects.add((str(p), ','.join(found)))
            folder_stat = p.stat()
            folders_batch.append((str(p), str(p.parent), p.name, folder_stat.st_ctime, folder_stat.st_mtime, len(p.parts), len(filenames), len(dirnames), 0, '', 'protected' if is_project else 'none', '', scan_time))
            for fn in filenames:
                fp = p / fn
                try:
                    st = fp.stat()
                except Exception as e:
                    logger(f'skip file stat: {fp} {e}')
                    continue
                cat, _ = classify(fp, rules, in_project=is_project)
                files_batch.append((str(fp), str(p), fp.name, fp.stem, fp.suffix.lower(), st.st_size, st.st_ctime, st.st_mtime, st.st_atime, str(root), len(fp.parts), None, cat, str(p) if is_project else None, str(p) if is_project else None, '', scan_time))
            if len(files_batch) >= batch_size:
                conn.executemany('INSERT OR REPLACE INTO files(full_path,parent_path,filename,stem,extension,size_bytes,created_time,modified_time,accessed_time,drive_root,depth,sha256_optional,category,project_group,protected_root,flags,scan_time) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', files_batch)
                files_batch.clear()
            if len(folders_batch) >= batch_size:
                conn.executemany('INSERT OR REPLACE INTO folders(full_path,parent_path,folder_name,created_time,modified_time,depth,file_count,folder_count,total_size_bytes,category,protected_status,flags,scan_time) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', folders_batch)
                folders_batch.clear()
    if files_batch:
        conn.executemany('INSERT OR REPLACE INTO files(full_path,parent_path,filename,stem,extension,size_bytes,created_time,modified_time,accessed_time,drive_root,depth,sha256_optional,category,project_group,protected_root,flags,scan_time) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', files_batch)
    if folders_batch:
        conn.executemany('INSERT OR REPLACE INTO folders(full_path,parent_path,folder_name,created_time,modified_time,depth,file_count,folder_count,total_size_bytes,category,protected_status,flags,scan_time) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', folders_batch)
    for rp, mk in projects:
        conn.execute('INSERT OR REPLACE INTO projects(root_path,project_name,project_type,confidence,detected_markers,protected_reason,scan_time) VALUES (?,?,?,?,?,?,?)', (rp, Path(rp).name, 'ProtectedProject', 0.9, mk, 'marker_detected', scan_time))
    conn.commit()
