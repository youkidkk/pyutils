from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Callable, Dict, List


class WalkResultType(Enum):
    Absolute = auto()
    FileNameOnly = auto()
    Relative = auto()


def _assert_is_directory(target: Path):
    """対象パスがディレクトリであることをチェックする"""
    if not target.exists():
        raise ValueError(f"対象パスが存在しません: {target}")
    if not target.is_dir():
        raise ValueError(f"対象パスがディレクトリではありません: {target}")


def walk(
    target_dir: Path | str,
    result_type: WalkResultType = WalkResultType.FileNameOnly,
    empty_dir: bool = False,
    dir_filter: Callable[[Path], bool] = lambda _: True,
    file_filter: Callable[[Path], bool] = lambda _: True,
) -> Dict[Path, List[Path]]:
    """ディレクトリ配下のディレクトリとその配下のファイルの Dict を取得"""
    target = Path(target_dir)
    _assert_is_directory(target)

    def conv_dir(dir: Path) -> Path:
        return dir if result_type != WalkResultType.Absolute else dir.absolute()

    def conv_file(file: Path, parent: Path) -> Path:
        return {
            WalkResultType.Absolute: (parent / file).absolute(),
            WalkResultType.FileNameOnly: Path(file),
            WalkResultType.Relative: parent / file,
        }[result_type]

    return {
        conv_dir(current_dir): [
            conv_file(file, current_dir)
            for file in files
            if file_filter(Path(current_dir) / file)
        ]
        for current_dir, _, files in target.walk()
        if (files or empty_dir) and dir_filter(Path(current_dir))
    }


def walk_files(
    target_dir: Path | str,
    absolute: bool = False,
    file_filter: Callable[[Path], bool] = lambda _: True,
) -> List[Path]:
    """ディレクトリ配下のファイルの List を取得"""
    target = Path(target_dir)
    _assert_is_directory(target)

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
            [(current := current / d) for d in dirs],  # noqa: F841
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
        current_path = root / current
        if any(current_path.iterdir()):
            break
        current_path.rmdir()
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
    target_path = Path(file_path)
    if not target_path.is_file():
        raise FileNotFoundError(
            f"ファイルが存在しないか、ファイルではありません: {file_path}"
        )
    stat = target_path.stat()

    # 更新日時
    mtime = datetime.fromtimestamp(stat.st_mtime)
    # 作成日時
    try:
        ctime = datetime.fromtimestamp(stat.st_birthtime)
    except AttributeError:
        # st_birthtime がサポートされていない環境（Linuxなど）では st_ctime を代用
        ctime = datetime.fromtimestamp(stat.st_ctime)

    return min(ctime, mtime)


if __name__ == "__main__":
    pass
