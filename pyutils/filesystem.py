import os
from pathlib import Path
from typing import Dict, List


def _normalize_path(path):
    sep = os.path.sep
    return path.replace("/", sep).replace("\\", sep)


def walk(parent_dir: str) -> Dict[str, List[str]]:
    return {
        _normalize_path(current_dir): files
        for current_dir, _, files in os.walk(parent_dir)
        if files
    }


def walk_files(parent_dir: str, relative=False) -> List[str]:
    def rel(path):
        if not relative:
            return path
        return str(Path(path).relative_to(Path(parent_dir)))

    return [
        _normalize_path(rel(os.path.join(current_dir, file)))
        for current_dir, _, files in os.walk(parent_dir)
        if files
        for file in files
    ]
