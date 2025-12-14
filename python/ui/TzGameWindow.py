from arcade import Window

from python.ui.TzViewManager import TzViewManager
from python.util.ConfigureUtil import ConfigureUtil
from python.util.I18nUtil import I18nUtil
from python.util.LanguageManager import LanguageManager

KEY_WINDOW_WIDTH: str = "window.width"
KEY_WINDOW_HEIGHT: str = "window.height"
KEY_WINDOW_TITLE_DEFAULT: str = "window.title.default"

def _get_window_title() -> str:
    """
    获取窗口标题
    :return: 窗口标题
    """
    return I18nUtil.get_main(KEY_WINDOW_TITLE_DEFAULT)


class TzGameWindow(Window):
    """
    主窗口
    :since: 2025-12-15
    """

    def __init__(self) -> None:
        """
        构造函数
        """
        width: int = ConfigureUtil.get_config(KEY_WINDOW_WIDTH)
        height: int = ConfigureUtil.get_config(KEY_WINDOW_HEIGHT)
        super().__init__(width, height, _get_window_title(), resizable=True)
        self.show_view(TzViewManager.get_current_view())

        def __on_language_changed() -> None:
            self.set_caption(_get_window_title())
        LanguageManager.on_change_language(__on_language_changed)

        def __on_view_changed() -> None:
            self.show_view(TzViewManager.get_current_view())
        TzViewManager.on_change_view("window_change_view", __on_view_changed)
