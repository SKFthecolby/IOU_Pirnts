from __future__ import annotations

def text_search(conn, term: str):
    return conn.execute('SELECT full_path, category, size_bytes FROM files WHERE lower(full_path) LIKE ?', (f'%{term.lower()}%',)).fetchall()

def by_ext(conn, ext: str):
    ext = ext.lower()
    if not ext.startswith('.'):
        ext = f'.{ext}'
    return conn.execute(
        'SELECT full_path, category, size_bytes FROM files WHERE extension=?',
        (ext,),
    ).fetchall()

def by_category(conn, category: str):
    return conn.execute('SELECT full_path, extension, size_bytes FROM files WHERE category=?', (category,)).fetchall()
