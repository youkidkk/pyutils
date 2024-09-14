import os
import shutil
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


def parent_dirs(
    target_dir: Union[Path, str],
    root_dir: Union[Path, str],
) -> Union[List[Path]]:
    target_absolute = Path(target_dir).resolve()
    root_absolute = Path(root_dir).resolve()
    try:
        dirs = [Path(d) for d in target_absolute.relative_to(root_absolute).parts]
        current = Path("")
        return sorted(
            [(current := current.joinpath(d)) for d in dirs],  # noqa: F841
            reverse=True,
        )
    except ValueError:
        return []


def remove_empty_parents(
    target_dir: Union[Path, str],
    root_dir: Union[Path, str],
) -> List[Path]:
    target = Path(target_dir)
    if target.is_file():
        return []
    root = Path(root_dir)
    deleted: List[Path] = []
    for current in parent_dirs(target, root):
        current_path = root.joinpath(current)
        if list(current_path.iterdir()):
            return deleted
        shutil.rmtree(current_path)
        deleted.append(current_path)
    return deleted


if __name__ == "__main__":
    pass
