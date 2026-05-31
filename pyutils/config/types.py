from abc import ABC, ABCMeta, abstractmethod
from pathlib import Path
from typing import Any


class FieldTypeBase(ABC):
    @classmethod
    @abstractmethod
    def _validate(cls, value: Any) -> Any:
        pass


class _PathBaseValidationMeta(ABCMeta):
    """isinstance(obj, Class) の挙動をカスタマイズするメタクラス"""

    def __instancecheck__(cls, instance: Any) -> bool:
        if not isinstance(instance, Path):
            return False
        try:
            cls._validate(instance)
            return True
        except ValueError:
            return False


class PathBase(FieldTypeBase, metaclass=_PathBaseValidationMeta):
    """パスを示す型"""

    def __new__(cls, org_value: Any) -> Path:
        return cls._validate(Path(org_value))

    @classmethod
    def _validate(cls, value: Path) -> Path:
        return value


class Directory(PathBase):
    """ディレクトリ型"""

    @classmethod
    def _validate(cls, value: Path) -> Path:
        value = super()._validate(value)
        if value.is_file():
            # ファイルである場合はエラー
            raise ValueError(f"対象パスがファイルとして存在します {value}")
        return value


class ExistingDirectory(Directory):
    """存在するディレクトリを示す型"""

    @classmethod
    def _validate(cls, value: Path) -> Path:
        value = super()._validate(value)
        if not value.is_dir():
            # ディレクトリとして存在しない場合はエラー
            raise ValueError(f"対象ディレクトリが存在しません {value}")
        return value


class EmptyDirectory(ExistingDirectory):
    """空のディレクトリを示す型"""

    @classmethod
    def _validate(cls, value: Path) -> Path:
        value = super()._validate(value)
        if any(value.iterdir()):
            # 空のディレクトリではない場合はエラー
            raise ValueError(f"対象ディレクトリが空ではありません {value}")
        return value


class EmptyOrNonExistingDirectory(Directory):
    """空または存在しないディレクトリを示す型"""

    @classmethod
    def _validate(cls, value: Path) -> Path:
        value = super()._validate(value)
        if value.is_dir() and any(value.iterdir()):
            # ディレクトリとして存在し、空ではない場合はエラー
            raise ValueError(f"対象ディレクトリが空ではありません {value}")
        return value


class File(PathBase):
    """ファイルを示す型"""

    @classmethod
    def _validate(cls, value: Path) -> Path:
        value = super()._validate(value)
        if value.is_dir():
            # ディレクトリである場合はエラー
            raise ValueError(f"対象パスがディレクトリとして存在します {value}")
        return value


class ExistingFile(File):
    """存在するファイルを示す型"""

    @classmethod
    def _validate(cls, value: Path) -> Path:
        value = super()._validate(value)
        if not value.is_file():
            # ファイルとして存在しない場合はエラー
            raise ValueError(f"対象ファイルが存在しません {value}")
        return value
