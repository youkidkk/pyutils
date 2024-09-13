import os
from pathlib import Path
from typing import Dict, List, Union


def _normalize_path(path):
    sep = os.path.sep
    return path.replace("/", sep).replace("\\", sep)


def walk(parent_dir: Union[Path, str]) -> Dict[Path, List[Path]]:
    target = Path(parent_dir)
    return {
        Path(_normalize_path(current_dir)): [Path(f) for f in files]
        for current_dir, _, files in os.walk(target)
        if files
    }


def walk_files(parent_dir: Union[Path, str], relative=False) -> List[Path]:
    def rel(path):
        if not relative:
            return path
        return Path(path).relative_to(Path(parent_dir))

    target = Path(parent_dir)
    return [
        Path(_normalize_path(rel(os.path.join(current_dir, file))))
        for current_dir, _, files in os.walk(target)
        if files
        for file in files
    ]


if __name__ == "__main__":
    pass
