from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import JSON
from config.db import db


class CrawlerConfig(db.Model):
    __tablename__ = 'crawler_configs'

    config_name = Column(String(100), primary_key=True)
    keywords = Column(JSON, nullable=False)
    website_names = Column(JSON, nullable=False)
    source_urls = Column(JSON, nullable=False)
    category = Column(String(50), nullable=False)
    created_user = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'config_name': self.config_name,
            'keywords': self.keywords,
            'website_names': self.website_names,
            'source_urls': self.source_urls,
            'category': self.category,
            'created_user': self.created_user,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
