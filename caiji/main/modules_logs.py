import logging
from logs.logger_config import LoggerConfig


def get_module_logger(
    module_name: str,
    base_dir: str = '../../logs',
    log_level: int = logging.INFO,
    include_console: bool = False
) -> logging.Logger:
    """
    为爬虫组件创建一个独立的日志记录器。

    Args:
        module_name: 模块/组件名
        base_dir: 日志根目录
        log_level: 日志级别
        include_console: 是否输出到控制台

    Returns:
        配置好的日志记录器
    """
    logger_name = f"caiji_modules_{module_name}"

    # 创建LoggerConfig实例
    config = LoggerConfig(
        base_dir=base_dir,
        log_level=log_level
    )

    service_name = f"crawler_{module_name}"

    # 创建并返回记录器
    logger = config.setup_logger(
        logger_name=logger_name,
        service_name=service_name,
        include_console=include_console
    )

    return logger
