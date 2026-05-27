from dataclasses import dataclass, fields
from pathlib import Path
from typing import Self

import yaml


@dataclass(frozen=True)
class ConfigBase:
    def __post_init__(self) -> None:
        for field in fields(self.__class__):
            object.__setattr__(
                self,
                field.name,
                field.type(getattr(self, field.name)),
            )
            if hasattr(field.type, "_validate"):
                field.type._validate(getattr(self, field.name))

    @classmethod
    def load(cls, config_path: Path = Path("./config.yaml")) -> Self:
        with open(config_path, encoding="utf-8") as config_file:
            config_dict = yaml.safe_load(config_file)
            return cls(**cls._convert(config_dict))

    @classmethod
    def _convert(cls, raw_dict: dict) -> dict:
        return raw_dict
