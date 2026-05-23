import math

import pytest

from pyutils.media.colors import Color


@pytest.mark.parametrize("r,g,b", [(1, 2, 3), (4, 8, 16)])
def test_Color_constructor(r, g, b):
    color = Color(r, g, b)
    assert color.red == r
    assert color.green == g
    assert color.blue == b
    assert color.alpha == 255


@pytest.mark.parametrize(
    "r,g,b,result",
    [
        (-1, 2, 3, Color(0, 2, 3)),
        (0, 2, 3, Color(0, 2, 3)),
        (255, 2, 3, Color(255, 2, 3)),
        (256, 2, 3, Color(255, 2, 3)),
        (1, -1, 3, Color(1, 0, 3)),
        (1, 0, 3, Color(1, 0, 3)),
        (1, 255, 3, Color(1, 255, 3)),
        (1, 256, 3, Color(1, 255, 3)),
        (1, 2, -1, Color(1, 2, 0)),
        (1, 2, -0, Color(1, 2, 0)),
        (1, 2, 255, Color(1, 2, 255)),
        (1, 2, 256, Color(1, 2, 255)),
    ],
)
def test_Color_constructor_exceed_limit(r, g, b, result):
    color = Color(r, g, b)
    assert color == result


@pytest.mark.parametrize(
    "c1,c2,result",
    [
        (Color(1, 2, 3, 100), Color(2, 4, 6, 100), math.sqrt(1 + 4 + 9)),
        (Color(4, 6, 8, 100), Color(1, 2, 3, 100), math.sqrt(9 + 16 + 25)),
    ],
)
def test_Color_distance(c1, c2, result):
    assert c1.distance(c2) == result
