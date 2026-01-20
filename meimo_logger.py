import logging
import os
from typing import override


class ColorFormatter(logging.Formatter):
    """控制台专用的彩色Formatter"""
    
    COLOR_CODES = {
        logging.INFO: '\033[92m',     # 绿色
        logging.WARNING: '\033[93m',  # 黄色
        logging.ERROR: '\033[91m',    # 红色
        logging.DEBUG: '\033[94m',    # 蓝色
        logging.CRITICAL: '\033[95m', # 紫色
    }
    
    RESET_CODE = '\033[0m'
    
    @override
    def format(self, record: logging.LogRecord) -> str:
        # 调用父类格式化
        message = super().format(record)
        
        # 只在控制台添加颜色
        color_code = self.COLOR_CODES.get(record.levelno)
        if color_code:
            # 为levelname添加颜色
            message = message.replace(
                f"{record.levelname}",
                f"{color_code}{record.levelname}{self.RESET_CODE}",
                1
            )
        return message


def setup_logger() -> logging.Logger:
    """设置日志记录器，包括控制台和文件处理器"""
    logger = logging.getLogger("魅魔AI自动签到")
    
    if logger.hasHandlers():
        return logger
    
    logger.setLevel(logging.INFO)
    
    from datetime import datetime, timedelta, timezone
    beijing_tz = timezone(timedelta(hours=8)) # 北京时间 UTC+8
    
    formatter = ColorFormatter('%(asctime)s (UTC+8) - %(name)s - %(levelname)s - %(message)s')
    file_formatter = logging.Formatter('%(asctime)s (UTC+8) - %(name)s - %(levelname)s - %(message)s')

    time_converter = lambda *_: datetime.now(beijing_tz).timetuple()
    formatter.converter = time_converter
    file_formatter.converter = time_converter

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    log_file = f'{logs_dir}/signin_{datetime.now(beijing_tz).strftime("%Y-%m-%d")}.log'
    
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)

    logger.addHandler(handler)
    logger.addHandler(file_handler)
    return logger
    