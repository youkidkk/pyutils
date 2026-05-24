import threading
from functools import wraps
from typing import Any, Callable, Type

# 型定義をより具体的に
_instances: dict[Type, Any] = {}
# シングルトン生成時の排他制御用ロック
_singleton_lock = threading.Lock()


def singleton(cls: Type) -> Callable[..., Any]:
    """シングルトンにするクラスデコレータ"""

    @wraps(cls)
    def getinstance(*args: Any, **kwargs: Any) -> Any:
        if cls not in _instances:
            with _singleton_lock:
                if cls not in _instances:
                    _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]

    return getinstance


def synchronized(func: Callable[..., Any]) -> Callable[..., Any]:
    """関数やメソッドの実行を同期化するデコレータ"""
    lock = threading.Lock()

    @wraps(func)
    def synced_function(*args: Any, **kwargs: Any) -> Any:
        with lock:
            return func(*args, **kwargs)

    return synced_function
