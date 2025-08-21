from datetime import datetime
from config.db import db
from app.models.heartbeat_model import Heartbeat


def send_caiji_heartbeat():
    """
    更新 heartbeat 表中的 caiji_heartbeat 字段（id=1）。
    """
    record = db.session.get(Heartbeat, 1)
    if record:
        record.caiji_heartbeat = datetime.utcnow()
        db.session.commit()
