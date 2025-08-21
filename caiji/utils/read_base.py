from datetime import datetime
from config.db import db
from app.models.base_crawler import BaseCrawler


def read_base(base_id: int = 1):
    """
    读取 base_crawler 表中指定 id 的记录。
    返回：(BaseCrawler 实例, switch_status, frequency)
    """
    session = db.session
    try:
        base = session.query(BaseCrawler).get(base_id)
        if base is None:
            raise ValueError(f"找不到 id={base_id} 的 BaseCrawler 配置")
        return base, base.switch_status, base.frequency
    finally:
        session.close()
