import logging
import os
import sys
from enum import Enum
from typing import Dict
from typing import Optional
from typing import Tuple

from pyjavaproperties import Properties

from python.util.LanguageManager import LanguageManager
from python.util.PgLoggerFactory import PgLoggerFactory

LOGGER: logging.Logger = PgLoggerFactory.get_logger(__name__)
PROPERTIES_ENCODING: str = "ISO-8859-1"

class ConfigureType(Enum):
    UI_CONFIG = "classpath:config/ui.properties"
    I18N_MAIN_CONFIG = "i18n:common.i18n.main"
    I18N_GAME_CONFIG = "i18n:common.i18n.game"

class ConfigureUtil:
    _configure_cache: Dict[ConfigureType, Dict[str, str | int | float | bool | Tuple[int, int, int]]] = {}

    @classmethod
    def on_change_language(cls) -> None:
        for configure_type in ConfigureType:
            if configure_type.value.startswith("i18n:") and configure_type in cls._configure_cache:
                cls._configure_cache.pop(configure_type)

    @classmethod
    def get_config(cls, key: str, resource_type: ConfigureType = ConfigureType.UI_CONFIG)\
            -> Optional[str | int | float | bool | Tuple[int, int, int]]:
        if resource_type is None or key is None or len(key.strip()) == 0:
            return None
        if resource_type not in cls._configure_cache:
            configure_file_path: str = cls.__get_resource_file_path(resource_type)
            configure_properties: Properties = Properties()
            with open(configure_file_path, "r", encoding=PROPERTIES_ENCODING) as configure_file:
                configure_properties.load(configure_file)
            configure_dict: Dict[str, str | int | float | bool | Tuple[int, int, int]] = {}
            for current_key, current_value in configure_properties.getPropertyDict().items():
                real_key, real_value = cls.__parse_configure_value(current_key, current_value)
                configure_dict[real_key] = real_value
            cls._configure_cache[resource_type] = configure_dict
        return cls._configure_cache[resource_type].get(key, None)

    @classmethod
    def __get_resource_file_path(cls, resource_type: ConfigureType) -> str:
        """
        根据资源类型获取配置文件
        :param resource_type: 资源类型
        :return: 配置文件所在路径
        """
        relative_path: str = resource_type.value
        if relative_path.startswith("classpath:"):
            relative_path: str = relative_path.removeprefix("classpath:")
        elif relative_path.startswith("i18n:"):
            relative_path: str = cls.get_config(relative_path.removeprefix("i18n:"), ConfigureType.UI_CONFIG)\
                .format(language=LanguageManager.get_current_language().value)
        return cls.__get_absolute_resource_file_path(relative_path)

    @classmethod
    def __parse_configure_value(cls, key: str, value: Optional[str])\
            -> Tuple[str, Optional[str | int | float | bool | Tuple[int, int, int]]]:
        if value is None:
            return key, None
        elif key.endswith(".str"):
            return key.removesuffix(".str"), cls.__decode_unicode_value(value)
        elif key.endswith(".int"):
            return key.removesuffix(".int"), int(value)
        elif key.endswith(".float"):
            return key.removesuffix(".float"), float(value)
        elif key.endswith(".bool"):
            return key.removesuffix(".bool"), bool(value)
        elif key.endswith(".tuple"):
            return key.removesuffix(".tuple"), (0, 0, 0)
        elif key.endswith(".file"):
            return key.removesuffix(".file"), cls.__get_absolute_resource_file_path(cls.__decode_unicode_value(value))
        return key, cls.__decode_unicode_value(value)

    @classmethod
    def __decode_unicode_value(cls, value: str) -> str:
        return value.encode(PROPERTIES_ENCODING).decode("unicode_escape")

    @classmethod
    def __get_absolute_resource_file_path(cls, relative_path: str) -> str:
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            base_dir = sys._MEIPASS
            resource_root = os.path.join(base_dir, "..", "resources")
        else:
            current_file_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_file_dir)
            resource_root = os.path.join(project_root, "..", "resources")
        full_path = os.path.normpath(os.path.join(resource_root, relative_path))
        if not os.path.exists(full_path):
            LOGGER.error(f"Resource file {full_path} not found.")
            raise FileNotFoundError(f"Resource file {full_path} not found.")
        LOGGER.info(f"Resource file {full_path} found.")
        return full_path

# 注册语言切换回调
LanguageManager.on_change_language(ConfigureUtil.on_change_language)
