import pytest

from pyutils.validation import *


@pytest.mark.parametrize(
    "value, required, expected",
    [
        (None, False, []),
        ("", False, []),
        (None, True, ["必須入力です"]),
        ("", True, ["必須入力です"]),
    ],
)
def test_validate_required(value, required, expected):
    assert validate(value, required=required) == expected


def test_validate_required_custom_message():
    assert validate("", required=True, required_error_msg="入力必須項目です") == [
        "入力必須項目です"
    ]


@pytest.mark.parametrize(
    "value, expected_type, expected_errors",
    [
        ("hello", str, []),
        (123, int, []),
        (123, str, ["型エラーです: int"]),
        ("hello", int, ["型エラーです: str"]),
        (True, int, ["型エラーです: bool"]),  # bool ガードの検証
        (True, bool, []),
    ],
)
def test_validate_expected_type(value, expected_type, expected_errors):
    assert validate(value, expected_type=expected_type) == expected_errors


def test_length_rule():
    # 5桁判定
    rule_func = length(5)
    assert rule_func("12345") is None
    assert rule_func("1234") == "5桁で入力してください"


def test_min_length_rule():
    # 3桁以上判定
    rule_func = min_length(3)
    assert rule_func("123") is None
    assert rule_func("12") == "3桁以上で入力してください"


def test_max_length_rule():
    # 5桁以下判定
    rule_func = max_length(5)
    assert rule_func("12345") is None
    assert rule_func("123456") == "5桁以下で入力してください"


def test_length_range_rule():
    # 2桁より大きく 5桁より小さい (3桁, 4桁がOK)
    rule_func = length_range(2, 5)
    assert rule_func("123") is None
    assert rule_func("12") == "2桁以上、5桁以下で入力してください"


def test_rule_custom_err_msg():
    rule_func = min_length(5, err_msg="5文字以上で指定してください")
    assert rule_func("123") == "5文字以上で指定してください"


def test_validate_interrupt():
    # 2つ目のルールで interrupt=True に設定
    rules = [
        min_length(3),  # OK (通過)
        max_length(5, interrupt=True),  # NG (エラー＆中断発生)
        length(4),  # 評価されない
    ]

    errors = validate("123456", rules=rules)

    # 2つ目のエラーメッセージのみが返され、3つ目は実行されていないこと
    assert len(errors) == 1
    assert errors == ["5桁以下で入力してください"]


def test_validate_multiple_rules_accumulate_errors():
    # interrupt なしの場合はエラーが集積されること
    rules = [
        min_length(5),  # NG
        max_length(3),  # NG
    ]

    errors = validate("1234", rules=rules)
    assert len(errors) == 2
    assert errors == ["5桁以上で入力してください", "3桁以下で入力してください"]
