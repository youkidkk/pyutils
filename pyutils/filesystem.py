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


def walk_files(
    target_dir: Path | str,
    absolute: bool = False,
) -> List[Path]:
    """ディレクトリ配下のファイルの List を取得"""
    target = Path(target_dir)
    if not target.exists() or target.is_file():
        raise ValueError(f"{target}: Not exist or Not directory")

    def conv_absolute(path: Path):
        return path.absolute() if absolute else path

    path_objs = target.glob("**/*")
    return [conv_absolute(obj) for obj in path_objs if obj.is_file()]


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
