import os
from typing import Dict, List


def walk(parent_dir: str) -> Dict[str, List[str]]:
    return {
        current_dir: files for current_dir, _, files in os.walk(parent_dir) if files
    }
