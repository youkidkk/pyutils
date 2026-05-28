from dataclasses import dataclass, fields
from pathlib import Path
from typing import Self

import yaml


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
            if hasattr(field.type, "_validate"):
                field.type._validate(getattr(self, field.name))

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
                    raise ValueError(f"設定ファイルの形式が不正です: {config_path}")

                # 項目の存在チェック
                non_existing_items = [
                    f.name for f in fields(cls) if f.name not in config_dict
                ]
                if any(non_existing_items):
                    raise ValueError(
                        f"""設定ファイルの項目が不足しています: {", ".join(non_existing_items)}"""
                    )

                return cls(**cls._convert(config_dict))
        except FileNotFoundError as e:
            raise FileNotFoundError(f"設定ファイルが見つかりません: {config_path}")

    @classmethod
    def _convert(cls, raw_dict: dict) -> dict:
        """
        設定ファイルからインスタンス変数に設定する型に変換する。
        何らかの変換が必要な場合、派生クラス側で処理を追加すること。
        """
        return raw_dict
