from dataclasses import dataclass, fields
from pathlib import Path
from typing import Self

import yaml


@dataclass(frozen=True)
class ConfigBase:
    def __post_init__(self) -> None:
        for field in fields(self.__class__):
            # フィールドに値を設定
            object.__setattr__(
                self,
                field.name,
                field.type(getattr(self, field.name)),
            )
            # フィールドのバリデーションを実施
            if hasattr(field.type, "_validate"):
                field.type._validate(getattr(self, field.name))

    @classmethod
    def load(cls, config_path: Path = Path("./config.yaml")) -> Self:
        """設定ファイルを読み込み、インスタンスを返却する。

        Args:
            raw_dict (dict, optional): 設定ファイルのパス。 デフォルト ./config.yaml

        Returns:
            Self: 設定クラスのインスタンス。
        """
        with open(config_path, encoding="utf-8") as config_file:
            config_dict = yaml.safe_load(config_file)
            return cls(**cls._convert(config_dict))

    @classmethod
    def _convert(cls, raw_dict: dict) -> dict:
        """
        設定ファイルからインスタンス変数に設定する型に変換する。
        何らかの変換が必要な場合、派生クラス側で処理を追加すること。
        """
        return raw_dict
