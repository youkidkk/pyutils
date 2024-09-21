import os
import shutil
from pathlib import Path
from typing import Dict, List, Union


def _normalize_path(path: str) -> Path:
    sep = os.path.sep
    return Path(path.replace("/", sep).replace("\\", sep))


def walk(
    target_dir: Path | str,
    empty_dir=False,
) -> Dict[Path, List[Path]]:
    """ディレクトリ配下のファイルが存在するディレクトリとその配下のファイルの Dict を取得"""
    target = Path(target_dir)
    return {
        _normalize_path(current_dir): [Path(f) for f in files]
        for current_dir, _, files in os.walk(target)
        if files or empty_dir
    }


def walk_files(parent_dir: Path | str, relative=False) -> List[Path]:
    """ディレクトリ配下のファイルの List を取得"""

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
    target_dir: Path | str,
    root_dir: Path | str,
) -> Union[List[Path]]:
    """対象ディレクトリからルートディレクトリまでのディレクトリの List を取得"""

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
    target_dir: Path | str,
    root_dir: Path | str,
) -> List[Path]:
    """対象ディレクトリからルートディレクトリまでの空のディレクトリを削除"""
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
