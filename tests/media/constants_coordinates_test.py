from pyutils.media.constants import Point, Rectangle, Size


def test_point():
    p1 = Point(1, 2)
    p2 = Point(1, 2)
    p3 = Point(3, 2)
    p4 = Point(1, 4)

    assert str(p1) == "(1, 2)"

    assert p1 == p2
    assert p1 != p3
    assert p1 != p4


def test_size():
    s1 = Size(1, 2)
    s2 = Size(1, 2)
    s3 = Size(3, 2)
    s4 = Size(1, 4)

    assert str(s1) == "(1 * 2)"

    assert s1 == s2
    assert s1 != s3
    assert s1 != s4

    assert s1 + s4 == Size(2, 6)
    assert s3 - s1 == Size(2, 0)


def test_rectangle():
    r1 = Rectangle(Point(1, 2), Size(3, 4))
    r2 = Rectangle(Point(1, 2), Size(3, 4))

    assert str(r1) == "(1, 2) - (4, 6) (3 * 4)"

    assert r1 == r2
    assert r1.end_point == Point(4, 6)
