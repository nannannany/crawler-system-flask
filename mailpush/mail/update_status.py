from datetime import datetime, timedelta
from app.models.crawl_results import CrawlResult
from config.db import db


def mark_results_pushed(results: list[CrawlResult]):
    """
    将传入的 CrawlResult 列表标记为已推送（is_pushed = 1）。
    返回实际更新的记录数。
    """
    if not results:
        return 0

    ids = [r.id for r in results]
    updated_count = db.session.query(CrawlResult) \
        .filter(CrawlResult.id.in_(ids)) \
        .update({'is_pushed': 1}, synchronize_session=False)

    db.session.commit()
    return updated_count


def mark_stale_results(hours: int = 24):
    """
    将所有 crawled_at 早于当前时间 hours 小时的结果，
    不论是否发送，都标记为已推送（is_pushed = 1）。
    返回实际更新的记录数。
    """
    threshold = datetime.utcnow() - timedelta(hours=hours)

    updated_count = db.session.query(CrawlResult) \
        .filter(CrawlResult.is_pushed == 0,
                CrawlResult.crawled_at < threshold) \
        .update({'is_pushed': 1}, synchronize_session=False)

    db.session.commit()
    return updated_count