import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

# 日志目录
LOG_DIR = "logs"
Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

# 日志文件路径
LOG_FILE = os.path.join(LOG_DIR, "telegram_bot.log")

# 日志格式
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 日志级别
LOG_LEVEL = logging.INFO

# 配置日志
def setup_logger(name: str = "telegram_bot") -> logging.Logger:
    """
    配置并返回一个日志记录器。

    Args:
        name (str): 日志记录器的名称，默认为 "telegram_bot"。

    Returns:
        logging.Logger: 配置好的日志记录器。
    """
    # 获取日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # 如果已经配置过处理器，直接返回
    if logger.handlers:
        return logger

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    console_handler.setFormatter(console_formatter)

    # 创建文件处理器（按大小滚动）
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setLevel(LOG_LEVEL)
    file_formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    file_handler.setFormatter(file_formatter)

    # 添加处理器到日志记录器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# 全局日志记录器
logger = setup_logger()
