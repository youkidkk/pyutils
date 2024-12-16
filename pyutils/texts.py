import unicodedata

FALSY_VALUES = ["false", "no", "off", "0"]


def width(text: str) -> int:
    """文字列の幅（半角:1、全角:2）を取得"""
    return sum([2 if unicodedata.east_asian_width(c) in "FWA" else 1 for c in text])


TRUTHY_VALUES = ["true", "yes", "on", "1"]


def truthy(target: str) -> bool:
    target = target.lower()
    return True if target in TRUTHY_VALUES else False


FALSY_VALUES = ["false", "no", "off", "0"]


def falsy(target: str) -> bool:
    target = target.lower()
    return True if target in FALSY_VALUES else False


def remove_ctrl_chars(target: str) -> str:
    return "".join(ch for ch in target if unicodedata.category(ch)[0] != "C")
