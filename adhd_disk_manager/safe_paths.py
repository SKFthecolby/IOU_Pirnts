from __future__ import annotations
from pathlib import Path
from typing import Iterable


def normalize(path: str | Path) -> Path:
    return Path(path).expanduser()


def contains_token(path: str | Path, tokens: Iterable[str]) -> bool:
    p = str(path).lower()
    return any(t.lower() in p for t in tokens)


def is_subpath(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except Exception:
        return False


def safe_destination(base: Path, relative: str) -> Path:
    rel = Path(relative)
    if rel.is_absolute():
        raise ValueError('relative destination must not be absolute')
    dest = (base / rel).resolve()
    if not is_subpath(dest, base.resolve()):
        raise ValueError('unsafe destination path escape')
    return dest
