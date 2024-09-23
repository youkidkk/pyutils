import threading
from typing import Any, Callable, Type

_instances = {}


def singleton(cls: Type) -> Any:
    """シングルトンのデコレータ"""

    def getinstance(*args, **kwargs) -> Any:
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]

    return getinstance


def synchronized(func: Callable) -> Callable:
    """同期処理のデコレータ"""
    func.__lock__ = threading.Lock()

    def synced_function(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return synced_function
