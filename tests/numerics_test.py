import pytest

from pyutils.numerics import ExceedLimitBehavior, Integer, is_integer


def test_is_integer():
    assert is_integer("123abc") is False
    assert is_integer(123) is True
    assert is_integer("123") is True
    assert is_integer(-123) is True
    assert is_integer("-123") is True
    assert is_integer(+123) is True
    assert is_integer("+123") is True
    assert is_integer(123.123) is False
    assert is_integer("123.123") is False


def test_Integer_constructor_normal():
    # 正常パターン
    Integer(123, 0, 200)
    assert True


@pytest.mark.parametrize("val,min,max", [("a", 0, 100), (0, "a", 100), (0, 0, "a")])
def test_Integer_constructor_arg_type(val, min, max):
    # 引数の型エラー
    with pytest.raises(ValueError) as e:
        Integer(val, min, max)
        assert str(e.value).startswith("Value should be int: ")


@pytest.mark.parametrize(
    "val,min,max,err",
    [
        # 最小値 > 最大値
        (0, 1, 0, "Min value exceeded max value: "),
        # 値 < 最小値
        (-1, 0, 100, "Min value exceeded: "),
        # 最大値 < 値
        (101, 0, 100, "Max value exceeded: "),
    ],
)
def test_Integer_constructor_arg_val(val, min, max, err):
    # exceed_limit_behavior = Default
    with pytest.raises(ValueError) as e:
        Integer(val, min, max)
        assert str(e.value).startswith(err)


@pytest.mark.parametrize(
    "val,min,max,err",
    [
        # 最小値 > 最大値
        (0, 1, 0, "Min value exceeded max value: "),
        # 値 < 最小値
        (-1, 0, 100, "Min value exceeded: "),
        # 最大値 < 値
        (101, 0, 100, "Max value exceeded: "),
    ],
)
def test_Integer_constructor_ExceedLimitBehavior_Raise(val, min, max, err):
    # exceed_limit_behavior = ExceedLimitBehavior.Raise
    with pytest.raises(ValueError) as e:
        Integer(val, min, max, ExceedLimitBehavior.Raise)
        assert str(e.value).startswith(err)


@pytest.mark.parametrize(
    "val,min,max,result_val",
    [
        # 値 < 最小値
        (-1, 0, 100, 0),
        # 最大値 < 値
        (101, 0, 100, 100),
    ],
)
def test_Integer_constructor_ExceedLimitBehavior_LimitValue(val, min, max, result_val):
    # exceed_limit_behavior = ExceedLimitBehavior.LimitValue
    i = Integer(val, min, max, ExceedLimitBehavior.LimitValue)
    assert i.value == result_val


@pytest.mark.parametrize(
    "val,min,max,result_min,result_max",
    [
        # 値 < 最小値
        (-1, 0, 100, -1, 100),
        # 最大値 < 値
        (101, 0, 100, 0, 101),
    ],
)
def test_Integer_constructor_ExceedLimitBehavior_Expand(
    val, min, max, result_min, result_max
):
    # exceed_limit_behavior = ExceedLimitBehavior.Expand
    i = Integer(val, min, max, ExceedLimitBehavior.Expand)
    assert i.min_value == result_min
    assert i.max_value == result_max


def test_Integer___str__():
    assert str(Integer(123)) == "123"


@pytest.mark.parametrize(
    "val1,val2,result", [(123, 123, True), (123, 124, False), (124, 123, False)]
)
def test_Integer___eq__(val1, val2, result):
    i1 = Integer(val1)
    i2 = Integer(val2)
    assert (i1 == i2) is result


@pytest.mark.parametrize(
    "val1,val2,result", [(123, 123, False), (123, 124, True), (124, 123, True)]
)
def test_Integer___ne__(val1, val2, result):
    i1 = Integer(val1)
    i2 = Integer(val2)
    assert (i1 != i2) is result


@pytest.mark.parametrize(
    "val1,val2,result", [(123, 124, True), (123, 123, False), (124, 123, False)]
)
def test_Integer___lt__(val1, val2, result):
    i1 = Integer(val1)
    i2 = Integer(val2)
    assert (i1 < i2) is result


@pytest.mark.parametrize(
    "val1,val2,result", [(123, 124, True), (123, 123, True), (124, 123, False)]
)
def test_Integer___le__(val1, val2, result):
    i1 = Integer(val1)
    i2 = Integer(val2)
    assert (i1 <= i2) is result


@pytest.mark.parametrize(
    "val1,val2,result", [(123, 124, False), (123, 123, False), (124, 123, True)]
)
def test_Integer___gt__(val1, val2, result):
    i1 = Integer(val1)
    i2 = Integer(val2)
    assert (i1 > i2) is result


@pytest.mark.parametrize(
    "val1,val2,result", [(123, 124, False), (123, 123, True), (124, 123, True)]
)
def test_Integer___ge__(val1, val2, result):
    i1 = Integer(val1)
    i2 = Integer(val2)
    assert (i1 >= i2) is result


@pytest.mark.parametrize(
    "val1,val2,result_val", [(123, 124, 247), (123, Integer(125), 248)]
)
def test_Integer___add__(val1, val2, result_val):
    i1 = Integer(val1, 0, 300)
    i2 = val2
    result = i1 + i2
    assert result.value == result_val
    assert result.min_value == i1.min_value
    assert result.max_value == i1.max_value


@pytest.mark.parametrize(
    "val1,val2,result_val", [(123, 124, 200), (123, Integer(125), 200)]
)
def test_Integer___add___ExceedLimitBehavior_LimitValue(val1, val2, result_val):
    i1 = Integer(val1, 0, 200, ExceedLimitBehavior.LimitValue)
    i2 = val2
    result = i1 + i2
    assert result.value == result_val
    assert result.min_value == i1.min_value
    assert result.max_value == i1.max_value


@pytest.mark.parametrize(
    "val1,val2,result_val", [(123, 124, 247), (123, Integer(125), 248)]
)
def test_Integer___add___ExceedLimitBehavior_Expand(val1, val2, result_val):
    i1 = Integer(val1, 0, 200, ExceedLimitBehavior.Expand)
    i2 = val2
    result = i1 + i2
    assert result.value == result_val
    assert result.min_value == i1.min_value
    assert result.max_value == result_val


@pytest.mark.parametrize(
    "val1,val2,result_val", [(234, 123, 111), (234, Integer(124), 110)]
)
def test_Integer___sub__(val1, val2, result_val):
    i1 = Integer(val1, 0, 300)
    i2 = val2
    result = i1 - i2
    assert result.value == result_val
    assert result.min_value == i1.min_value
    assert result.max_value == i1.max_value


@pytest.mark.parametrize(
    "val1,val2,result_val", [(234, 123, 111), (234, Integer(124), 110)]
)
def test_Integer___sub___ExceedLimitBehavior_LimitValue(val1, val2, result_val):
    i1 = Integer(val1, 200, 300, ExceedLimitBehavior.LimitValue)
    i2 = val2
    result = i1 - i2
    assert result.value == i1.min_value
    assert result.min_value == i1.min_value
    assert result.max_value == i1.max_value


@pytest.mark.parametrize(
    "val1,val2,result_val", [(234, 123, 111), (234, Integer(124), 110)]
)
def test_Integer___sub___ExceedLimitBehavior_Expand(val1, val2, result_val):
    i1 = Integer(val1, 200, 300, ExceedLimitBehavior.Expand)
    i2 = val2
    result = i1 - i2
    assert result.value == result_val
    assert result.min_value == result_val
    assert result.max_value == i1.max_value


def test_Integer___mul__():
    i1 = Integer(123, 0, 10000)
    i2 = Integer(3)
    result = i1 * i2
    assert result.value == i1.value * i2.value
    assert result.min_value == i1.min_value
    assert result.max_value == i1.max_value


def test_Integer___truediv__():
    i1 = Integer(100, 0, 10000)
    i2 = Integer(3)
    result = i1 / i2
    assert result == i1.value / i2.value


def test_Integer___floordiv__():
    i1 = Integer(100, 0, 10000)
    i2 = Integer(3)
    result = i1 // i2
    assert result.value == i1.value // i2.value
    assert result.min_value == i1.min_value
    assert result.max_value == i1.max_value


def test_Integer___mod__():
    i1 = Integer(100, 0, 10000)
    i2 = Integer(3)
    result = i1 % i2
    assert result.value == i1.value % i2.value
    assert result.min_value == i1.min_value
    assert result.max_value == i1.max_value


def test_Integer___pow__():
    i1 = Integer(10, 0, 10000)
    i2 = Integer(3)
    result = i1**i2
    assert result.value == i1.value**i2.value
    assert result.min_value == i1.min_value
    assert result.max_value == i1.max_value
