from config.db import db
from datetime import datetime


class CrawlPool(db.Model):
    __tablename__ = 'crawl_pool'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100),nullable=False)
    source_url = db.Column(db.String(500), nullable=False)
    keyword = db.Column(db.String(100), nullable=False)
    config_names = db.Column(db.JSON, nullable=False, default=[])
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    website_names = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'category':self.category,
            'source_url': self.source_url,
            'keyword': self.keyword,
            'config_names': self.config_names,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'website_names': self.website_names
        }
