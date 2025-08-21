from datetime import datetime, timedelta
from config.db import db
from app.models.base_crawler import BaseCrawler


def mark_running(base_id: int, frequency_hours: int):
    """
    爬虫开始前调用：
    - crawler_status = 2
    - next_run_time = now + frequency_hours
    """
    session = db.session
    try:
        base = session.query(BaseCrawler).get(base_id)
        if base is None:
            raise ValueError(f"找不到 id={base_id} 的 BaseCrawler 配置")
        base.crawler_status = 2
        base.next_run_time = datetime.utcnow() + timedelta(hours=frequency_hours)
        session.commit()
    finally:
        session.close()


def mark_idle(base_id: int):
    """
    爬虫完成后调用：
    - crawler_status = 1
    """
    session = db.session
    try:
        base = session.query(BaseCrawler).get(base_id)
        if base is None:
            raise ValueError(f"找不到 id={base_id} 的 BaseCrawler 配置")
        base.crawler_status = 1
        session.commit()
    finally:
        session.close()
