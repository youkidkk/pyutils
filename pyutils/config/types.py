from pathlib import Path


class Directory(Path):
    """ディレクトリ型"""

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

    @classmethod
    def _validate(cls, value: Path) -> None:
        if value.is_file():
            # ファイルである場合はエラー
            raise ValueError(f"対象パスがファイルとして存在します {value}")


class ExistingDirectory(Directory):
    """存在するディレクトリを示す型"""

    @classmethod
    def _validate(cls, value: Path) -> None:
        super()._validate(value)
        if not value.is_dir():
            # ディレクトリとして存在しない場合はエラー
            raise ValueError(f"対象ディレクトリが存在しません {value}")


class EmptyDirectory(ExistingDirectory):
    """空のディレクトリを示す型"""

    @classmethod
    def _validate(cls, value: Path) -> None:
        super()._validate(value)
        if any(value.iterdir()):
            # 空のディレクトリではない場合はエラー
            raise ValueError(f"対象ディレクトリが空ではありません {value}")


class EmptyOrNonExistingDirectory(Directory):
    """空または存在しないディレクトリを示す型"""

    @classmethod
    def _validate(cls, value: Path) -> None:
        super()._validate(value)
        if value.is_dir() and any(value.iterdir()):
            # ディレクトリとして存在し、空ではない場合はエラー
            raise ValueError(f"対象ディレクトリが空ではありません {value}")


class File(Path):
    """ファイル型"""

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

    @classmethod
    def _validate(cls, value: Path) -> None:
        if value.is_dir():
            # ディレクトリである場合はエラー
            raise ValueError(f"対象パスがディレクトリとして存在します {value}")


class ExistingFile(File):
    """存在するファイルを示す型"""

    @classmethod
    def _validate(cls, value: Path) -> None:
        super()._validate(value)
        if not value.is_file():
            # ファイルとして存在しない場合はエラー
            raise ValueError(f"対象ファイルが存在しません {value}")
