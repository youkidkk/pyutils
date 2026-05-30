from dataclasses import MISSING, dataclass, field, fields
from pathlib import Path
from typing import Self

import yaml


class ConfigValidateError(ValueError):
    def __init__(self, message: str, errors: dict[str, str]):
        super().__init__(message)
        self.errors = errors

    def __str__(self):
        err_texts = [f"{key}: {err}" for key, err in self.errors.items()]
        return (
            f"""{super().__str__()}\n{"\n".join(["  " + err for err in err_texts])}"""
        )


@dataclass(frozen=True)
class ConfigBase:
    def __post_init__(self) -> None:
        for field in fields(self.__class__):
            # フィールド値の型変換
            object.__setattr__(
                self,
                field.name,
                field.type(getattr(self, field.name)),
            )

        # フィールドのバリデーションを実施
        error_items = {}
        for field in fields(self.__class__):
            try:
                if hasattr(field.type, "_validate"):
                    field.type._validate(getattr(self, field.name))
            except ValueError as e:
                error_items[field.name] = str(e)
        if error_items:
            raise ConfigValidateError("項目値が不正です", error_items)

    @classmethod
    def from_dict(cls, config_dict: dict, source_type="設定") -> Self:
        # 項目の存在チェック
        non_existing_items = [
            f.name
            for f in fields(cls)
            if f.name not in config_dict
            and (f.default is MISSING and f.default_factory is MISSING)
        ]
        if any(non_existing_items):
            raise ValueError(
                f"""{source_type}の項目が不足しています: {", ".join(non_existing_items)}"""
            )
        return cls(**cls._convert(config_dict))

    @classmethod
    def from_yaml(cls, config_path: Path = Path("./config.yaml")) -> Self:
        """設定ファイルを読み込み、インスタンスを返却する。

        Args:
            config_path (dict, optional): 設定ファイルのパス。 デフォルト ./config.yaml

        Returns:
            Self: 設定クラスのインスタンス。
        """
        try:
            with config_path.open(encoding="utf-8") as config_file:
                config_dict = yaml.safe_load(config_file)
                if not config_dict:
                    raise ValueError(f"設定ファイルの形式が不正です {config_path}")
                return cls.from_dict(config_dict, source_type="設定ファイル")
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"設定ファイルが見つかりません: {config_path}"
            ) from e
        except ConfigValidateError as e:
            raise ConfigValidateError(
                f"設定ファイルの項目値が不正です {config_path}",
                e.errors,
            ) from e

    @classmethod
    def _convert(cls, raw_dict: dict) -> dict:
        """
        設定ファイルからインスタンス変数に設定する型に変換する。
        何らかの変換が必要な場合、派生クラス側で処理を追加すること。
        """
        return raw_dict
