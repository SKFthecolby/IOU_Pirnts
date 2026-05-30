from __future__ import annotations
from itertools import combinations


def detect_duplicates(conn):
    rows = conn.execute('SELECT full_path,size_bytes FROM files WHERE size_bytes>0 ORDER BY size_bytes, full_path').fetchall()
    by_size = {}
    for r in rows:
        by_size.setdefault(r['size_bytes'], []).append(r['full_path'])

    out = []
    for sz, items in by_size.items():
        if len(items) > 1:
            for a, b in combinations(items, 2):
                out.append(('size_match', a, b, sz, 0, 0.0, 'candidate only'))
    if out:
        conn.executemany('INSERT INTO duplicates(match_type,file_a,file_b,size_bytes,hash_match,name_similarity,warning) VALUES (?,?,?,?,?,?,?)', out)
        conn.commit()
    return out
