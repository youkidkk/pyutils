from pathlib import Path


class Directory:
    def __init__(self, arg: Path | str):
        self._value = Path(arg)

    def __getattr__(self, name):
        return getattr(self._value, name)

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


class File:
    def __init__(self, arg: Path | str):
        self._value = Path(arg)

    def __getattr__(self, name):
        return getattr(self._value, name)

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
