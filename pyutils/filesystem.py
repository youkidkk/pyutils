import os
import shutil
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Callable, Dict, List


def _normalize_path(path: str) -> Path:
    sep = os.path.sep
    return Path(path.replace("/", sep).replace("\\", sep))


class WalkResultType(Enum):
    Absolute = auto()
    FileNameOnly = auto()
    Relative = auto()


def walk(
    target_dir: Path | str,
    result_type: WalkResultType = WalkResultType.FileNameOnly,
    empty_dir: bool = False,
    dir_filter: Callable[[Path], bool] = lambda _: True,
    file_filter: Callable[[Path], bool] = lambda _: True,
) -> Dict[Path, List[Path]]:
    """ディレクトリ配下のディレクトリとその配下のファイルの Dict を取得"""
    target = Path(target_dir)
    if not target.exists() or target.is_file():
        raise ValueError(f"{target}: Not exist or Not directory")

    def conv_dir(dir: str) -> Path:
        normalized = _normalize_path(dir)
        return (
            normalized
            if result_type != WalkResultType.Absolute
            else normalized.absolute()
        )

    def conv_file(filename: str, parent: str) -> Path:
        parent = _normalize_path(parent)
        return {
            WalkResultType.Absolute: parent.joinpath(filename).absolute(),
            WalkResultType.FileNameOnly: Path(filename),
            WalkResultType.Relative: parent.joinpath(filename),
        }[result_type]

    return {
        conv_dir(current_dir): [
            conv_file(file, current_dir)
            for file in files
            if file_filter(Path(current_dir).joinpath(file))
        ]
        for current_dir, _, files in os.walk(target)
        if (files or empty_dir) and dir_filter(Path(current_dir))
    }


def walk_files(
    target_dir: Path | str,
    absolute: bool = False,
    file_filter: Callable[[Path], bool] = lambda _: True,
) -> List[Path]:
    """ディレクトリ配下のファイルの List を取得"""
    target = _normalize_path(str(target_dir))
    if not target.exists() or target.is_file():
        raise ValueError(f"{target}: Not exist or Not directory")

    def conv_absolute(path: Path):
        return path.absolute() if absolute else path

    path_objs = target.glob("**/*")
    return sorted(
        [conv_absolute(obj) for obj in path_objs if obj.is_file() and file_filter(obj)]
    )


def parent_dirs(
    target_dir: Path | str,
    root_dir: Path | str,
    absolute: bool = False,
) -> List[Path]:
    """対象ディレクトリからルートディレクトリまでのディレクトリの List を取得"""

    target_absolute = Path(target_dir).resolve()
    root_absolute = Path(root_dir).resolve()
    try:
        dirs = [Path(d) for d in target_absolute.relative_to(root_absolute).parts]
        current = Path("")
        result = sorted(
            [(current := current.joinpath(d)) for d in dirs],  # noqa: F841
            reverse=True,
        )
        if absolute:
            result = [r.absolute() for r in result]
        return result
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


def get_older_file_timestamp(file_path: Path | str) -> datetime:
    """指定したファイルの作成日時と更新日時を比較し、より古い方の日時を返す。

    Args:
        file_path (Path | str): 対象ファイルのパス（Pathオブジェクトまたは文字列）。

    Returns:
        datetime: タイムゾーンなし(naive)の、古い方の日時オブジェクト。

    Raises:
        FileNotFoundError: ファイルが存在しないか、ファイルではない場合。
    """
    # 1. Pathオブジェクトに変換して一元化
    target_path = Path(file_path)

    # 2. ファイルの存在確認（ディレクトリなどの場合は弾く）
    if not target_path.is_file():
        raise FileNotFoundError(
            f"ファイルが存在しないか、ファイルではありません: {file_path}"
        )

    # 3. ファイルのメタデータ（stat）を取得
    stat = target_path.stat()

    # 4. 更新日時の取得
    mtime = datetime.fromtimestamp(stat.st_mtime)

    # 5. 作成日時の取得（OSによる挙動の違いを安全に吸収）
    try:
        ctime = datetime.fromtimestamp(stat.st_birthtime)
    except AttributeError:
        # st_birthtime がサポートされていない環境（Linuxなど）では st_ctime を代用
        ctime = datetime.fromtimestamp(stat.st_ctime)

    # 6. 2つの日時を比較し、古い方を返却
    return min(ctime, mtime)


if __name__ == "__main__":
    pass
