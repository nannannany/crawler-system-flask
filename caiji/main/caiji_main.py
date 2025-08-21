import logging
import time
from datetime import datetime
import threading
from logs.logger_config import LoggerConfig
from caiji.utils.read_base import read_base
from caiji.utils.operate_base import mark_running, mark_idle
from caiji.utils.send_heartbeat import send_caiji_heartbeat
from caiji.utils.pool_synchronization import sync_crawler_config_to_pool
from caiji.main.keyword_transmit import run_spiders_from_pool
from app import create_app

app = create_app()
BASE_ID = 1


def heartbeat_loop(logger):
    """每30秒发送一次爬虫心跳"""
    with app.app_context():
        while True:
            try:
                send_caiji_heartbeat()
                logger.info(f"发送心跳")
            except Exception as e:
                logger.info(f"发送心跳异常: {e}")
            time.sleep(30)


def main():
    # 初始化日志配置
    log_config = LoggerConfig(
        base_dir='logs',
        log_level=logging.INFO
    )
    logger = log_config.setup_logger(
        logger_name='run_caiji',
        service_name='crawler_main',
        include_console=True
    )
    logger.propagate = False
    logger.info("爬虫循环运行开始...")

    # 启动心跳线程
    threading.Thread(target=heartbeat_loop, args=(logger,), daemon=True).start()

    while True:
        try:
            base, switch_status, frequency = read_base(BASE_ID)
            now = datetime.utcnow()

            if switch_status != 1:
                logger.info("爬虫开关关闭，等待中...")
                time.sleep(60)
                continue

            next_run_time = base.next_run_time
            if not next_run_time or now >= next_run_time.replace(tzinfo=None):
                # 标记运行中并设置下次运行时间
                try:
                    mark_running(base.id, frequency)
                    logger.info(f"开始爬取，设置下次运行时间为当前时间 + {frequency} 小时")
                except Exception:
                    logger.exception("标记运行状态失败")
                    time.sleep(60)
                    continue

                try:
                    # 调用pool_synchronization.py
                    result = sync_crawler_config_to_pool(logger)
                    logger.info(f"Pool同步完成: {result}")
                    # 调用拆分出来的爬虫函数
                    run_spiders_from_pool(logger)
                except Exception:
                    logger.exception("爬虫运行中发生异常")
                finally:
                    try:
                        mark_idle(base.id)
                        logger.info("爬虫状态已重置为空闲")
                    except Exception:
                        logger.exception("重置爬虫状态失败")

            else:
                # 还未到运行时间
                wait_minutes = int((next_run_time - now).total_seconds() // 60)
                logger.info(f"未到下次运行时间（{next_run_time}），剩余约 {wait_minutes} 分钟")
                mark_idle(base.id)
                logger.info("爬虫状态已重置为空闲")
                time.sleep(min(60, wait_minutes * 60))

        except Exception as e:
            logger.exception(f"循环中出现异常：{e}")
            time.sleep(60)