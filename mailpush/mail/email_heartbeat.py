import time
import threading
from datetime import datetime
from config.db import db
from app.models.heartbeat_model import Heartbeat
from logs.logger_config import get_logger


class EmailHeartbeat:
    def __init__(self, app):
        self.running = False
        self.thread = None
        self.app = app
        self.logger = get_logger(__name__)

    def start_heartbeat(self):
        """启动心跳"""
        self.running = True
        self.thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self.thread.start()
        self.logger.info("Email心跳已启动")

    def _heartbeat_loop(self):
        """心跳循环"""
        while self.running:
            try:
                with self.app.app_context():
                    self._update_heartbeat()
                time.sleep(30)  # 每30秒执行一次
            except Exception as e:
                self.logger.error(f"心跳更新失败: {e}")
                time.sleep(30)

    def _update_heartbeat(self):
        """更新心跳数据"""
        try:
            heartbeat = Heartbeat.query.first()

            if not heartbeat:
                heartbeat = Heartbeat()
                db.session.add(heartbeat)

            heartbeat.email_heartbeat = datetime.utcnow()
            heartbeat.email_status = 1

            db.session.commit()
            self.logger.info(f"Email心跳更新成功: {datetime.utcnow()}")

        except Exception as e:
            db.session.rollback()
            raise e