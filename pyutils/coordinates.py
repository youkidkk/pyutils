from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Size:
    width: int
    height: int

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

    @property
    def end_point(self):
        return Point(
            self.start_point.x + self.size.width,
            self.start_point.y + self.size.height,
        )
