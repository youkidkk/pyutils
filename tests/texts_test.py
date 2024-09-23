import pytest

from pyutils import texts


def test_width():
    assert texts.width("あいうえお12345") == 15


class TestTruthy:
    @pytest.fixture(
        params=[
            ["true", True],
            ["TRUE", True],
            ["yes", True],
            ["YES", True],
            ["on", True],
            ["ON", True],
            ["1", True],
            ["false", False],
            ["no", False],
            ["off", False],
            ["0", False],
        ]
    )
    def pattern(self, request):
        return texts.truthy(request.param[0]) == request.param[1]

    def test(self, pattern):
        assert pattern


def test_remove_ctrl_chars():
    func = texts.remove_ctrl_chars
    assert func("12\n3\r a\tb\bc") == "123 abc"
