import os
from dataclasses import dataclass
from enum import Enum, auto
from typing import Self


def is_integer(value: int | str) -> bool:
    if type(value) is int:
        return True
    try:
        float(value)
    except ValueError:
        return False
    else:
        return float(value).is_integer()


class ExceedLimitBehavior(Enum):
    Raise = auto()
    LimitValue = auto()
    Expand = auto()


_env_min_str = os.environ.get("NUMBER_DEFAULT_MIN_VALUE")
DEFAULT_MIN_VALUE = int(_env_min_str) if is_integer(_env_min_str) else -999999999
_env_max_str = os.environ.get("NUMBER_DEFAULT_MAX_VALUE")
DEFAULT_MAX_VALUE = int(_env_max_str) if is_integer(_env_max_str) else 999999999


@dataclass(frozen=True)
class Number:
    value: int = 0
    min_value: int = DEFAULT_MIN_VALUE
    max_value: int = DEFAULT_MAX_VALUE
    exceed_limit_behavior: ExceedLimitBehavior = ExceedLimitBehavior.Raise

    def __post_init__(self):
        if not all(
            [
                type(v) is int
                for v in [
                    self.value,
                    self.min_value,
                    self.max_value,
                ]
            ]
        ):
            # 引数の型エラー
            raise ValueError(
                "Value should be int: "
                f"{self.value=}, {self.min_value=}, {self.max_value}"
            )
        if self.min_value > self.max_value:
            # 最小値 > 最大値はエラー
            raise ValueError(
                "Min value exceeded max value: " f"{self.min_value=}, {self.max_value}"
            )
        if self.value < self.min_value:
            # 値 < 最小値
            match self.exceed_limit_behavior:
                case ExceedLimitBehavior.Raise:
                    raise ValueError(
                        "Min value exceeded: " f"{self.value=}, {self.min_value=}"
                    )
                case ExceedLimitBehavior.LimitValue:
                    object.__setattr__(self, "value", self.min_value)
                case ExceedLimitBehavior.Expand:
                    object.__setattr__(self, "min_value", self.value)
        if self.max_value < self.value:
            # 最大値 < 値
            match self.exceed_limit_behavior:
                case ExceedLimitBehavior.Raise:
                    raise ValueError(
                        "Max value exceeded: " f"{self.value=}, {self.max_value=}"
                    )
                case ExceedLimitBehavior.LimitValue:
                    object.__setattr__(self, "value", self.max_value)
                case ExceedLimitBehavior.Expand:
                    object.__setattr__(self, "max_value", self.value)

    def __to_number(self, value: int | Self) -> Self:
        if type(value) is Number:
            return value
        elif type(value) is int:
            return Number(value)
        raise ValueError(f"Value should be Number or int: {type(value)}")

    def __str__(self):
        return str(self.value)

    def __eq__(self, other: int | Self):
        # = 演算子
        return self.value == self.__to_number(other).value

    def __ne__(self, other: int | Self):
        # != 演算子
        return self.value != self.__to_number(other).value

    def __lt__(self, other: int | Self):
        # < 演算子
        return self.value < self.__to_number(other).value

    def __le__(self, other: int | Self):
        # <= 演算子
        return self.value <= self.__to_number(other).value

    def __gt__(self, other: int | Self):
        # > 演算子
        return self.value > self.__to_number(other).value

    def __ge__(self, other: int | Self):
        # >= 演算子
        return self.value >= self.__to_number(other).value

    def __add__(self, other: int | Self) -> Self:
        # + 演算子
        other = self.__to_number(other)
        return Number(
            self.value + other.value,
            self.min_value,
            self.max_value,
            self.exceed_limit_behavior,
        )

    def __sub__(self, other: int | Self) -> Self:
        # - 演算子
        other = self.__to_number(other)
        return Number(
            self.value - other.value,
            self.min_value,
            self.max_value,
            self.exceed_limit_behavior,
        )

    def __mul__(self, other: int | Self) -> Self:
        # * 演算子
        other = self.__to_number(other)
        return Number(
            self.value * other.value,
            self.min_value,
            self.max_value,
            self.exceed_limit_behavior,
        )

    def __truediv__(self, other: int | Self) -> float:
        # / 演算子 -> float型を返却
        other = self.__to_number(other)
        return self.value / other.value

    def __floordiv__(self, other: int | Self) -> Self:
        # // 演算子
        other = self.__to_number(other)
        return Number(
            self.value // other.value,
            self.min_value,
            self.max_value,
            self.exceed_limit_behavior,
        )

    def __mod__(self, other: int | Self) -> Self:
        # % 演算子
        other = self.__to_number(other)
        return Number(
            self.value % other.value,
            self.min_value,
            self.max_value,
            self.exceed_limit_behavior,
        )

    def __pow__(self, other: int | Self) -> Self:
        # ** 演算子
        other = self.__to_number(other)
        return Number(
            self.value**other.value,
            self.min_value,
            self.max_value,
            self.exceed_limit_behavior,
        )
