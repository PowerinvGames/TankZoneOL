import logging
import sys
from typing import Dict

LOGGER_CACHE: Dict[str, logging.Logger] = {}
LOGGER_FORMATTER_CONSOLE: str = "%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"

class PgLoggerFactory:
    """
    日志记录器工厂
    :since: 2025-12-12
    """

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        获取指定名称的日志记录器
        :param name: 日志记录器名称
        """
        if name not in LOGGER_CACHE:
            # 新建一个logger对象
            result_logger: logging.Logger = logging.getLogger(name)
            result_logger.setLevel(logging.INFO)

            # 新建一个控制台处理器，并设置为追加写入模式
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)

            # 新建一个格式化输出器
            formatter = logging.Formatter(LOGGER_FORMATTER_CONSOLE)
            console_handler.setFormatter(formatter)

            # 将文件处理器添加到logger中
            result_logger.addHandler(console_handler)
            LOGGER_CACHE[name] = result_logger

        return LOGGER_CACHE[name]
