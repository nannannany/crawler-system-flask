from config.db import db
from datetime import datetime


class CrawlResult(db.Model):
    __tablename__ = 'crawl_results'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    config_name = db.Column(db.String(100), nullable=False)
    keyword = db.Column(db.String(100), nullable=False)
    website_name = db.Column(db.String(100), nullable=False)
    source_url = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    detail_url = db.Column(db.String(500), nullable=False, unique=True)
    publish_time = db.Column(db.DateTime, nullable=True)
    publisher = db.Column(db.String(200), nullable=True)
    is_pushed = db.Column(db.Integer, nullable=False, default=0)
    crawled_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'config_name': self.config_name,
            'keyword': self.keyword,
            'website_name': self.website_name,
            'source_url': self.source_url,
            'title': self.title,
            'detail_url': self.detail_url,
            'publish_time': self.publish_time.isoformat() if self.publish_time else None,
            'publisher': self.publisher,
            'is_pushed': self.is_pushed,
            'crawled_at': self.crawled_at.isoformat() if self.crawled_at else None
        }
