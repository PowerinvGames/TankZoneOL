import arcade

from python.util.ConfigureUtil import ConfigureUtil
from python.util.I18nUtil import I18nUtil
from python.util.LanguageManager import Language
from python.util.LanguageManager import LanguageManager


class GameWindow(arcade.Window):
    def __init__(self, width: int, height: int, title_i18n: str) -> None:
        window_title: str = I18nUtil.get_main(title_i18n)
        super().__init__(width, height, window_title)

        def __on_language_changed() -> None:
            self.set_caption(I18nUtil.get_main(title_i18n))
        LanguageManager.on_change_language(__on_language_changed)

if __name__ == "__main__":
    window_width: int = ConfigureUtil.get_config("window.width")
    window_height: int = ConfigureUtil.get_config("window.height")
    game_window: GameWindow = GameWindow(window_width, window_height, "window.title.default")
    LanguageManager.change_language(Language.EN_US)
    font_file: str = ConfigureUtil.get_config("common.fonts.harmonyossans.regular")
    print(font_file)
    game_window.run()
