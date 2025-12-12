from typing import Optional

from python.util.ConfigureUtil import ConfigureType
from python.util.ConfigureUtil import ConfigureUtil


class I18nUtil:
    @staticmethod
    def get_main(key: str) -> Optional[str]:
        return ConfigureUtil.get_config(key, ConfigureType.I18N_MAIN_CONFIG)

    @staticmethod
    def get_game(key: str) -> Optional[str]:
        return ConfigureUtil.get_config(key, ConfigureType.I18N_GAME_CONFIG)
