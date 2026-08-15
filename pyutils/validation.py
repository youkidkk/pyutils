from collections.abc import Callable
from functools import wraps
from typing import Any


class InterruptValidation(Exception):
    """バリデーション処理を途中で中断するための例外"""


def _str_format(str_tmpl, *args, **kwargs):
    try:
        return str_tmpl.format(*args, **kwargs)
    except (IndexError, KeyError):
        return str_tmpl


def rule(err_msg_default: str, interrupt_default: bool = False):
    """バリデーション関数をルール化するデコレータ"""

    def decorator(func: Callable[..., bool]):
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Callable[[Any], str | None]:
            err_msg_tmpl = kwargs.pop("err_msg", err_msg_default)
            interrupt = kwargs.pop("interrupt", interrupt_default)

            def validator(value: Any) -> str | None:
                if func(value, *args, **kwargs):
                    return None

                # エラーメッセージの生成
                err = _str_format(err_msg_tmpl, *args, value=value, **kwargs)

                if interrupt:
                    raise InterruptValidation(err)
                return err

            return validator

        return wrapper

    return decorator


# --- ルール定義 ---


@rule("{0}桁で入力してください")
def length(value: str, len_: int) -> bool:
    return len(value) == len_


@rule("{0}桁以上で入力してください")
def min_length(value: str, len_: int) -> bool:
    return len(value) >= len_


@rule("{0}桁以下で入力してください")
def max_length(value: str, len_: int) -> bool:
    return len(value) <= len_


# --- バリデーション関数 ---


def validate(
    value: Any,
    required: bool = False,
    expected_type: type = str,
    rules: list[Callable[[Any], str | None]] | None = None,
    required_error_msg: str = "必須入力です",
    type_error_msg: str = "型エラーです: {0}",
) -> list[str]:
    # 必須チェック
    if value is None or value == "":
        if required:
            return [required_error_msg]
        else:
            return []

    # 型チェック
    if (expected_type is not bool and isinstance(value, bool)) or not isinstance(
        value, expected_type
    ):
        return [_str_format(type_error_msg, type(value).__name__)]

    # ルール検証
    if not rules:
        return []

    errors: list[str] = []
    try:
        for r in rules:
            if err := r(value):
                errors.append(err)
    except InterruptValidation as e:
        errors.append(str(e))

    return errors
