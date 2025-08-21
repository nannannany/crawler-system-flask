from app.models.crawl_results import CrawlResult
from app.models.users_model import User
from config.db import db


def fetch_pending_results():
    """
    返回所有 is_pushed = 0 的爬取结果列表。
    """
    return CrawlResult.query.filter_by(is_pushed=0).all()


def fetch_active_users():
    """
    返回所有 push_switch = 1 的用户列表。
    """
    return User.query.filter_by(push_switch=1).all()


def build_user_notifications():
    """
    构建每个用户的待推送结果映射：
      { user: [CrawlResult, ...], ... }
    CrawlResult.config_name 字符串类型，
    当该字符串与 User.push_categories 中的任一项匹配时，
    才认为该条结果需要推送给该用户。
    """
    results = fetch_pending_results()
    users = fetch_active_users()
    notifications = {}

    for user in users:
        # 用户订阅的类别列表
        user_categories = set(user.push_categories or [])

        # 筛选匹配的结果
        matched = [
            r for r in results
            if r.config_name and r.config_name in user_categories
        ]

        if matched:
            notifications[user] = matched

    return notifications