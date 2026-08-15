from collections.abc import Callable
from functools import wraps
from typing import Any


class InterruptValidation(Exception):
    """バリデーション処理を途中で中断するための例外"""


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
                try:
                    err = err_msg_tmpl.format(*args, value=value, **kwargs)
                except (IndexError, KeyError):
                    err = err_msg_tmpl

                if interrupt:
                    raise InterruptValidation(err)
                return err

            return validator

        return wrapper

    return decorator


@rule("{0}桁で入力してください")
def length(value: str, len_: int) -> bool:
    return len(value) == len_


@rule("{0}桁以上で入力してください")
def min_length(value: str, len_: int) -> bool:
    return len(value) >= len_


@rule("{0}桁以下で入力してください")
def max_length(value: str, len_: int) -> bool:
    return len(value) <= len_


def validate(
    value: Any,
    required=False,
    rules: list[Callable[[Any], str | None]] | None = None,
) -> list[str]:
    errors: list[str] = []
    if value is None or value == "":
        if required:
            return ["必須入力です"]
        else:
            return errors
    if not rules:
        return errors
    try:
        for r in rules:
            if err := r(value):
                errors.append(err)
    except InterruptValidation as e:
        errors.append(str(e))
    return errors
