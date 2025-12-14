import logging
import os
import re
import sys
from enum import Enum
from typing import Dict, List, Optional, Tuple, TypeAlias

from pyjavaproperties import Properties

from python.util.LanguageManager import LanguageManager
from python.util.PgLoggerFactory import PgLoggerFactory

LOGGER: logging.Logger = PgLoggerFactory.get_logger(__name__)
PROPERTIES_ENCODING: str = "ISO-8859-1"

# 类型别名定义
ColorType: TypeAlias = Tuple[int, int, int] | Tuple[int, int, int, int]
ConfigValueType: TypeAlias = str | int | float | bool | ColorType


class ConfigureType(Enum):
    """
    配置类型枚举类
    :since: 2025-12-13
    """
    UI_CONFIG = "classpath:config/ui.properties"
    I18N_MAIN_CONFIG = "i18n:common.i18n.main"
    I18N_GAME_CONFIG = "i18n:common.i18n.game"

class ConfigureUtil:
    """
    配置文件解析工具类
    :since: 2025-12-13
    """

    _configure_cache: Dict[ConfigureType, Dict[str, ConfigValueType]] = {}

    @classmethod
    def on_change_language(cls) -> None:
        """
        语言切换回调，删除已缓存的国际化键值对
        """
        for configure_type in ConfigureType:
            if configure_type.value.startswith("i18n:") and configure_type in cls._configure_cache:
                cls._configure_cache.pop(configure_type)

    @classmethod
    def get_config(cls, key: str, resource_type: ConfigureType = ConfigureType.UI_CONFIG) -> Optional[ConfigValueType]:
        """
        获取配置
        :param key: 键
        :param resource_type: 配置类型
        :return: 配置值
        """
        if resource_type is None or key is None or len(key.strip()) == 0:
            return None
        if resource_type not in cls._configure_cache:
            configure_file_path: str = cls.__get_resource_file_path(resource_type)
            configure_properties: Properties = Properties()
            with open(configure_file_path, "r", encoding=PROPERTIES_ENCODING) as configure_file:
                configure_properties.load(configure_file)
            configure_dict: Dict[str, ConfigValueType] = {}
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
        return cls.__get_absolute_resource_path(relative_path)

    @classmethod
    def __parse_configure_value(cls, key: str, value: Optional[str]) -> Tuple[str, Optional[ConfigValueType]]:
        """
        解析配置后缀，转换值类型
        :param key: 键
        :param value: 原始字符串值
        :return: 转换类型后的值
        """
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
        elif key.endswith(".color"):
            return key.removesuffix(".color"), cls.__format_color_value(value.strip())
        elif key.endswith(".file"):
            return key.removesuffix(".file"), cls.__get_absolute_resource_path(cls.__decode_unicode_value(value))
        return key, cls.__decode_unicode_value(value)

    @classmethod
    def __decode_unicode_value(cls, value: str) -> str:
        """
        Unicode解码
        :param value: ISO-8859-1编码的值
        :return: 经过Unicode解码后UTF-8编码的值
        """
        return value.encode(PROPERTIES_ENCODING).decode("unicode_escape")

    @classmethod
    def __format_color_value(cls, value: str) -> Optional[ColorType]:
        """
        解析并转换颜色类型
        :param value: 颜色类型字符串
        :return: RGB/RGBA颜色元组
        """
        if value.startswith("#"):
            if len(value) == 4:
                return int(value[1] * 2, 16), int(value[2] * 2, 16), int(value[3] * 2, 16) # RGB
            if len(value) == 7:
                return int(value[1:3], 16), int(value[3:5], 16), int(value[5:], 16) # RRGGBB
            elif len(value) == 9:
                return int(value[1:3], 16), int(value[3:5], 16), int(value[5:7], 16), int(value[7:], 16) # RRGGBBAA
        result: List[int] = [0, 0, 0, 255]
        numbers = re.findall(r"-?\d+(?:\.\d+)?", value)
        for i in range(min(len(numbers), 4)):
            result[i] = int(max(0, min(255, int(numbers[i]))))
        return result[0], result[1], result[2], result[3] # (RRR, GGG, BBB, AAA)

    @classmethod
    def __get_absolute_resource_path(cls, relative_path: str) -> str:
        """
        根据资源URI获取资源文件绝对路径
        :param relative_path: 资源URI
        :return: 资源文件绝对路径
        """
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
