from abc import ABC, abstractmethod
from pathlib import Path
from typing import Self


class FieldTypeBase(ABC):
    def __init__(self: Self, value: any) -> None:
        self._value = value

    @abstractmethod
    def _validate(self) -> None:
        pass

    def __call__(self: Self) -> any:
        return self._value


class PathBase(FieldTypeBase):
    """パスを示す型"""

    def __init__(self: Self, value: str) -> None:
        self._value = Path(value)

    def _validate(self) -> None:
        super()._validate()

    def __getattr__(self, name):
        """self._value(Pathオブジェクト)への移譲"""
        return getattr(self._value, name)


class Directory(PathBase):
    """ディレクトリ型"""

    def _validate(self) -> None:
        super()._validate()
        if self().is_file():
            # ファイルである場合はエラー
            raise ValueError(f"対象パスがファイルとして存在します {self()}")


class ExistingDirectory(Directory):
    """存在するディレクトリを示す型"""

    def _validate(self) -> None:
        super()._validate()
        if not self().is_dir():
            # ディレクトリとして存在しない場合はエラー
            raise ValueError(f"対象ディレクトリが存在しません {self()}")


class EmptyDirectory(ExistingDirectory):
    """空のディレクトリを示す型"""

    def _validate(self) -> None:
        super()._validate()
        if any(self().iterdir()):
            # 空のディレクトリではない場合はエラー
            raise ValueError(f"対象ディレクトリが空ではありません {self()}")


class EmptyOrNonExistingDirectory(Directory):
    """空または存在しないディレクトリを示す型"""

    def _validate(self) -> None:
        super()._validate()
        if self().is_dir() and any(self().iterdir()):
            # ディレクトリとして存在し、空ではない場合はエラー
            raise ValueError(f"対象ディレクトリが空ではありません {self()}")


class File(PathBase):
    """ファイルを示す型"""

    def _validate(self) -> None:
        super()._validate()
        if self().is_dir():
            # ディレクトリである場合はエラー
            raise ValueError(f"対象パスがディレクトリとして存在します {self()}")


class ExistingFile(File):
    """存在するファイルを示す型"""

    def _validate(self) -> None:
        super()._validate()
        if not self().is_file():
            # ファイルとして存在しない場合はエラー
            raise ValueError(f"対象ファイルが存在しません {self()}")
