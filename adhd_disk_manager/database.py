from __future__ import annotations
import sqlite3
from pathlib import Path

SCHEMA = [
"""CREATE TABLE IF NOT EXISTS files (
id INTEGER PRIMARY KEY, full_path TEXT UNIQUE, parent_path TEXT, filename TEXT, stem TEXT, extension TEXT,
size_bytes INTEGER, created_time REAL, modified_time REAL, accessed_time REAL, drive_root TEXT,
depth INTEGER, sha256_optional TEXT, category TEXT, project_group TEXT, protected_root TEXT, flags TEXT, scan_time TEXT)""",
"""CREATE TABLE IF NOT EXISTS folders (
id INTEGER PRIMARY KEY, full_path TEXT UNIQUE, parent_path TEXT, folder_name TEXT,
created_time REAL, modified_time REAL, depth INTEGER, file_count INTEGER, folder_count INTEGER,
total_size_bytes INTEGER, category TEXT, protected_status TEXT, flags TEXT, scan_time TEXT)""",
"""CREATE TABLE IF NOT EXISTS projects (
id INTEGER PRIMARY KEY, root_path TEXT UNIQUE, project_name TEXT, project_type TEXT, confidence REAL,
detected_markers TEXT, protected_reason TEXT, scan_time TEXT)""",
"""CREATE TABLE IF NOT EXISTS move_batches (
batch_id TEXT PRIMARY KEY, created_time TEXT, executed_time TEXT, status TEXT, total_items INTEGER,
moved_items INTEGER, failed_items INTEGER, total_size_bytes INTEGER, rollback_manifest TEXT)""",
"""CREATE TABLE IF NOT EXISTS move_items (
id INTEGER PRIMARY KEY, batch_id TEXT, source_path TEXT, destination_path TEXT, item_type TEXT,
category TEXT, matched_rule TEXT, approved INTEGER, status TEXT, error TEXT)""",
"""CREATE TABLE IF NOT EXISTS duplicates (
id INTEGER PRIMARY KEY, match_type TEXT, file_a TEXT, file_b TEXT, size_bytes INTEGER,
hash_match INTEGER, name_similarity REAL, warning TEXT)""",
]


def connect(db_path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    for s in SCHEMA:
        conn.execute(s)
    conn.commit()
    return conn
