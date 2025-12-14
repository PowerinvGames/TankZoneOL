import threading
from abc import ABC

from arcade import View


class TzAbstractView(View, ABC):
    """
    单例视图基类
    :since: 2025-12-15
    """

    _instance = None
    _lock = threading.RLock()  # 使用可重入锁

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls(*args, **kwargs)
        return cls._instance
