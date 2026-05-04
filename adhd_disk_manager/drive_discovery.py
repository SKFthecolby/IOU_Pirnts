from __future__ import annotations
import string
from pathlib import Path


def list_windows_drives() -> list[str]:
    drives = []
    for l in string.ascii_uppercase:
        p = Path(f"{l}:/")
        if p.exists():
            drives.append(f"{l}:")
    if not drives:
        drives.append(str(Path('/').resolve()))
    return drives


def select_roots(all_drives: bool, drive: str|None, roots: list[str]|None, excluded: list[str]) -> list[Path]:
    out = []
    if roots:
        out.extend(Path(r) for r in roots)
    elif drive:
        out.append(Path(drive + '/'))
    elif all_drives:
        out.extend(Path(d + '/') for d in list_windows_drives() if d not in excluded)
    return [p for p in out if p.exists()]
