import logging
from enum import Enum
from typing import Callable, Dict, Optional

from python.ui.TzAbstractView import TzAbstractView
from python.ui.splash.TzSplashView import TzSplashView
from python.util.PgLoggerFactory import PgLoggerFactory

LOGGER: logging.Logger = PgLoggerFactory.get_logger(__name__)


class TzViewType(Enum):
    SPLASH = TzSplashView
    MAIN = TzSplashView
    GAME = TzSplashView

class TzViewManager:
    """
    视图管理器
    :since: 2025-12-15
    """

    _current_view: TzViewType = TzViewType.SPLASH
    _view_cache: Dict[TzViewType, TzAbstractView] = {}
    _on_change_callbacks: Dict[str, Callable[[], None]] = {}

    @classmethod
    def on_change_view(cls, callback_key: str, callback: Callable[[], None]) -> None:
        """
        添加视图切换回调
        :param callback_key: 回调函数名称
        :param callback: 回调函数
        """
        if callback_key is not None and len(callback_key) > 0 and callback_key not in cls._on_change_callbacks:
            cls._on_change_callbacks[callback_key] = callback

    @classmethod
    def remove_change_view(cls, callback_key: str) -> None:
        """
        移除视图切换回调
        :param callback_key: 回调函数名称
        """
        if callback_key is not None and len(callback_key) > 0 and callback_key in cls._on_change_callbacks:
            cls._on_change_callbacks.pop(callback_key)

    @classmethod
    def register(cls, view_type: TzViewType, view: TzAbstractView) -> None:
        if view_type in cls._view_cache:
            LOGGER.warning(f"Duplicate view type: {view_type}, old view will be overwritten.")
        cls._view_cache[view_type] = view

    @classmethod
    def get_current_view(cls) -> TzAbstractView:
        if cls._current_view not in cls._view_cache:
            LOGGER.info(f"Creating {cls._current_view} view in view manager.")
            cls.register(cls._current_view, cls._current_view.value.get_instance())
        return cls._view_cache.get(cls._current_view)

    @classmethod
    def change_view(cls, view_type: TzViewType) -> bool:
        if view_type is None or view_type not in cls._view_cache:
            LOGGER.warning(f"View {view_type} is not registered, changing view failed.")
            return False
        cls._current_view = view_type
        for _, callback in cls._on_change_callbacks.items():
            callback()
        return True
