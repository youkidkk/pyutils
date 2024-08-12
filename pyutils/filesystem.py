import os
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
