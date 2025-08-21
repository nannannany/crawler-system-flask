import time
import threading
from datetime import datetime, timezone

from config.db import db
from app.models.heartbeat_model import Heartbeat
from app.models.base_crawler import BaseCrawler


def start_heartbeat_monitor_caiji(app):
    def monitor():
        with app.app_context():
            while True:
                try:
                    heartbeat = Heartbeat.query.first()
                    if heartbeat and heartbeat.caiji_heartbeat:
                        now = datetime.now(timezone.utc)
                        db.session.expire_all()
                        heartbeat_time = heartbeat.caiji_heartbeat

                        if heartbeat_time.tzinfo is None:
                            heartbeat_time = heartbeat_time.replace(tzinfo=timezone.utc)

                        diff = (now - heartbeat_time).total_seconds()
                        if diff > 60:
                            print(
                                f"[{datetime.now(timezone.utc).isoformat()}] [HEARTBEAT] BASE心跳超时，重置 BaseCrawler 状态为 0")
                            print(f"数据库心跳时间: {heartbeat.caiji_heartbeat}")
                            BaseCrawler.query.update({BaseCrawler.crawler_status: 0})
                            db.session.commit()
                        else:
                            print(f"[{datetime.now(timezone.utc).isoformat()}][HEARTBEAT] BASE正常，间隔 {diff:.1f} 秒")
                            print(f"数据库心跳时间: {heartbeat.caiji_heartbeat}")
                    else:
                        print("[HEARTBEAT] BASE无心跳记录")

                except Exception as e:
                    print(f"[HEARTBEAT] BASE错误: {e}")

                time.sleep(30)

    thread = threading.Thread(target=monitor, daemon=True)
    thread.start()
