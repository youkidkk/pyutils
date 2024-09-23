import threading
from typing import Any, Callable, Type


def singleton(cls: Type) -> Any:
    """シングルトンのデコレータ"""
    instances = {}

    def getinstance(*args, **kwargs) -> Any:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return getinstance


def synchronized(func: Callable) -> Callable:
    """同期処理のデコレータ"""
    func.__lock__ = threading.Lock()

    def synced_function(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return synced_function
