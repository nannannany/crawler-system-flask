import time
import threading
from datetime import datetime, timezone
from config.db import db
from app.models.heartbeat_model import Heartbeat


def start_heartbeat_monitor_mail(app):
    def monitor():
        with app.app_context():
            while True:
                try:
                    heartbeat = Heartbeat.query.first()
                    if heartbeat and heartbeat.email_heartbeat:
                        now = datetime.now(timezone.utc)
                        db.session.expire_all()
                        heartbeat_time = heartbeat.email_heartbeat
                        if heartbeat_time.tzinfo is None:
                            heartbeat_time = heartbeat_time.replace(tzinfo=timezone.utc)
                        diff = (now - heartbeat_time).total_seconds()
                        if diff > 60:
                            print(
                                f"[{datetime.now(timezone.utc).isoformat()}] [HEARTBEAT] Email心跳超时，重置状态为 0")
                            print(f"数据库心跳时间: {heartbeat.email_heartbeat}")
                            heartbeat.email_status = 0
                            db.session.commit()
                        else:
                            print(f"[{datetime.now(timezone.utc).isoformat()}][HEARTBEAT] Email正常，间隔 {diff:.1f} 秒")
                            print(f"数据库心跳时间: {heartbeat.email_heartbeat}")
                    else:
                        print("[HEARTBEAT] 无Email心跳记录")
                except Exception as e:
                    print(f"[HEARTBEAT] Email监控错误: {e}")
                time.sleep(30)

    thread = threading.Thread(target=monitor, daemon=True)
    thread.start()
