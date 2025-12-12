from enum import Enum
from typing import Callable
from typing import List


class Language(Enum):
    ZH_CN = "zh_CN"
    EN_US = "en_US"

class LanguageManager:
    """
    语言管理器
    :since: 2025-12-13
    """

    _current_language: Language = Language.ZH_CN
    _on_change_callbacks: List[Callable[[], None]] = []

    @classmethod
    def on_change_language(cls, callback: Callable[[], None]) -> None:
        """
        添加语言切换回调
        :param callback: 回调函数
        """
        if callback is not None and callback not in cls._on_change_callbacks:
            cls._on_change_callbacks.append(callback)

    @classmethod
    def remove_change_language(cls, callback: Callable[[], None]) -> None:
        """
        移除语言切换回调
        :param callback: 回调函数
        """
        if callback is not None and callback in cls._on_change_callbacks:
            cls._on_change_callbacks.remove(callback)

    @classmethod
    def get_current_language(cls) -> Language:
        """
        获取当前应用设置语言
        :return: 语言
        """
        return cls._current_language

    @classmethod
    def change_language(cls, language: Language = Language.ZH_CN) -> Language:
        """
        更新当前应用设置语言
        :param language: 目标语言
        :return: 旧的语言
        """
        old_language = cls._current_language
        cls._current_language = language if language is not None else Language.ZH_CN
        for callback in cls._on_change_callbacks:
            callback()
        return old_language
