import unicodedata

TRUTHY_VALUES = {"true", "yes", "y", "on", "1"}
FALSY_VALUES = {"false", "no", "n", "off", "0"}


def width(text: str) -> int:
    """文字列の幅（半角:1、全角:2）を取得"""

    return sum(2 if unicodedata.east_asian_width(c) in "FWA" else 1 for c in text)


def truthy(target: str) -> bool:
    """文字列が真価を表す値かどうかを判定"""
    return target.lower() in TRUTHY_VALUES


def falsy(target: str) -> bool:
    """文字列が偽価を表す値かどうかを判定"""
    return target.lower() in FALSY_VALUES


def remove_ctrl_chars(target: str) -> str:
    """制御文字を除去"""
    return "".join(ch for ch in target if unicodedata.category(ch)[0] != "C")
