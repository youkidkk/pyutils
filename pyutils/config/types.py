from pathlib import Path


class Directory(Path):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

    @classmethod
    def _validate(cls, value: Path) -> None:
        if value.is_file():
            raise ValueError(f"{value}: 対象パスがファイルとして存在します。")


class ExistingDirectory(Directory):
    @classmethod
    def _validate(cls, value: Path) -> None:
        super()._validate(value)
        if not value.is_dir():
            raise ValueError(f"{value}: 対象ディレクトリが存在しません。")


class EmptyDirectory(ExistingDirectory):
    @classmethod
    def _validate(cls, value: Path) -> None:
        super()._validate(value)
        if any(value.iterdir()):
            raise ValueError(f"{value}: 対象ディレクトリが空ではありません。")


class EmptyOrNonExistingDirectory(Directory):
    @classmethod
    def _validate(cls, value: Path) -> None:
        super()._validate(value)
        if value.is_dir() and any(value.iterdir()):
            raise ValueError(f"{value}: 対象ディレクトリが空ではありません。")


class File(Path):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

    @classmethod
    def _validate(cls, value: Path) -> None:
        if value.is_dir():
            raise ValueError(f"{value}: 対象パスがディレクトリとして存在します。")


class ExistingFile(File):
    @classmethod
    def _validate(cls, value: Path) -> None:
        super()._validate(value)
        if not value.is_file():
            raise ValueError(f"{value}: 対象ファイルが存在しません。")
