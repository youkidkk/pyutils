import unicodedata

TRUTHY_VALUES = ["true", "yes", "on", "1"]


def width(text):
    """文字列の幅（半角:1、全角:2）を取得"""
    return sum([2 if unicodedata.east_asian_width(c) in "FWA" else 1 for c in text])


def truthy(target: str):
    target = target.lower()
    return True if target in TRUTHY_VALUES else False
