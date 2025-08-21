import logging
import os
import datetime
from typing import Optional


class LoggerConfig:
    """日志配置管理类"""

    def __init__(self,
                 base_dir: str = 'logs',
                 log_level: int = logging.INFO,
                 date_format: str = '%Y-%m-%d %H:%M:%S',
                 encoding: str = 'utf-8'):
        """
        初始化日志配置

        Args:
            base_dir: 日志根目录，默认为 'logs'
            log_level: 日志级别，默认为 INFO
            date_format: 时间格式，默认为 '%Y-%m-%d %H:%M:%S'
            encoding: 文件编码，默认为 'utf-8'
        """
        self.base_dir = base_dir
        self.log_level = log_level
        self.date_format = date_format
        self.encoding = encoding
        self._logger_initialized = False

    def _get_log_file_path(self, service_name: str = 'mail') -> str:
        """
        生成日志文件路径

        Args:
            service_name: 服务名称，用于日志文件命名

        Returns:
            完整的日志文件路径
        """
        now = datetime.datetime.now()
        year_month = now.strftime('%Y_%m')  # 2025_01
        day_str = now.strftime('%d')  # 01, 02, ..., 31

        # 创建日志目录：logs/2025_08/
        log_dir = os.path.join(self.base_dir, year_month)
        os.makedirs(log_dir, exist_ok=True)

        # 日志文件名：01day_mail_log.txt
        log_filename = f"{day_str}day_{service_name}_log.txt"
        return os.path.join(log_dir, log_filename)

    def setup_logger(self,
                     logger_name: Optional[str] = None,
                     service_name: str = 'mail',
                     include_console: bool = False) -> logging.Logger:
        """
        配置并返回日志记录器

        Args:
            logger_name: 日志记录器名称，默认为 None（根记录器）
            service_name: 服务名称，用于日志文件命名
            include_console: 是否同时输出到控制台

        Returns:
            配置好的日志记录器
        """
        # 获取日志文件路径
        log_file_path = self._get_log_file_path(service_name)

        # 配置日志格式
        formatter = logging.Formatter(
            fmt='[%(asctime)s] %(levelname)s %(name)s: %(message)s',
            datefmt=self.date_format
        )

        # 获取或创建日志记录器
        if logger_name:
            logger = logging.getLogger(logger_name)
        else:
            logger = logging.getLogger()

        logger.setLevel(self.log_level)

        # 避免重复添加处理器
        if not self._logger_initialized:
            # 清除现有处理器
            logger.handlers.clear()

            # 文件处理器
            file_handler = logging.FileHandler(log_file_path, encoding=self.encoding)
            file_handler.setLevel(self.log_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            # 控制台处理器
            if include_console:
                import sys
                console_handler = logging.StreamHandler(sys.stdout)
                console_handler.setLevel(self.log_level)
                console_handler.setFormatter(formatter)
                logger.addHandler(console_handler)

            self._logger_initialized = True

        return logger

    def get_log_file_info(self, service_name: str = 'mail') -> dict:
        """
        获取当前日志文件信息

        Args:
            service_name: 服务名称

        Returns:
            包含日志文件路径等信息的字典
        """
        log_file_path = self._get_log_file_path(service_name)
        return {
            'log_file_path': log_file_path,
            'log_dir': os.path.dirname(log_file_path),
            'log_filename': os.path.basename(log_file_path),
            'exists': os.path.exists(log_file_path)
        }


# 便捷函数
def setup_mail_logger(base_dir: str = 'logs',
                      log_level: int = logging.INFO,
                      include_console: bool = False) -> logging.Logger:
    """
    快速配置邮件服务日志记录器

    Args:
        base_dir: 日志根目录
        log_level: 日志级别
        include_console: 是否输出到控制台

    Returns:
        配置好的日志记录器
    """
    config = LoggerConfig(base_dir=base_dir, log_level=log_level)
    return config.setup_logger(service_name='mail', include_console=include_console)


def get_logger(name: str) -> logging.Logger:
    """
    获取指定名称的日志记录器

    Args:
        name: 日志记录器名称

    Returns:
        日志记录器实例
    """
    return logging.getLogger(name)
