from __future__ import annotations
from pathlib import Path


def detect_project_root(path: Path, markers: list[str]) -> tuple[bool, list[str]]:
    found = []
    for m in markers:
        if (path / m).exists():
            found.append(m)
    return (len(found) > 0, found)
