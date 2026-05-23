import math
from dataclasses import dataclass
from typing import Self

from pyutils.numerics import ExceedLimitBehavior, Integer


class Color:
    def __init__(self, red, green, blue, alpha=255):
        self._red = Integer(red, 0, 255, ExceedLimitBehavior.LimitValue)
        self._green = Integer(green, 0, 255, ExceedLimitBehavior.LimitValue)
        self._blue = Integer(blue, 0, 255, ExceedLimitBehavior.LimitValue)
        self._alpha = Integer(alpha, 0, 255, ExceedLimitBehavior.LimitValue)

    @property
    def rgb(self):
        return self._red, self._green, self._blue

    @property
    def rgba(self):
        return self._red, self._green, self._blue, self._alpha

    @property
    def red(self):
        return self._red.value

    @property
    def green(self):
        return self._green.value

    @property
    def blue(self):
        return self._blue.value

    @property
    def alpha(self):
        return self._alpha.value

    def __eq__(self, other: Self) -> bool:
        return (
            self.red == other.red
            and self.green == other.green
            and self.blue == other.blue
            and self.alpha == other.alpha
        )

    def distance(self, other: Self) -> float:
        return math.sqrt(
            (abs(self.red - other.red) ** 2)
            + (abs(self.green - other.green) ** 2)
            + (abs(self.blue - other.blue) ** 2)
        )


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __str__(self):
        return f"({self.x}, {self.y})"


@dataclass(frozen=True)
class Size:
    width: int
    height: int

    def __str__(self):
        return f"({self.width} * {self.height})"

    def __add__(self, other):
        return Size(
            self.width + other.width,
            self.height + other.height,
        )

    def __sub__(self, other):
        return Size(
            self.width - other.width,
            self.height - other.height,
        )


@dataclass(frozen=True)
class Rectangle:
    start_point: Point
    size: Size

    def __str__(self):
        return f"{self.start_point} - {self.end_point} {self.size}"

    @property
    def end_point(self):
        return Point(
            self.start_point.x + self.size.width,
            self.start_point.y + self.size.height,
        )
