from python.ui.TzGameWindow import TzGameWindow
from python.util.ConfigureUtil import ConfigureUtil
from python.util.LanguageManager import Language, LanguageManager


if __name__ == "__main__":
    game_window: TzGameWindow = TzGameWindow()
    LanguageManager.change_language(Language.EN_US)
    font_file: str = ConfigureUtil.get_config("common.fonts.harmonyossans.regular")
    print(font_file)
    game_window.run()
