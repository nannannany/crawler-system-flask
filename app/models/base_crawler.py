from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from config.db import db


class BaseCrawler(db.Model):
    __tablename__ = 'base_crawlers'

    id = Column(Integer, primary_key=True)
    switch_status = Column(Integer, nullable=False, default=0)
    frequency = Column(Integer, nullable=False, default=1)
    crawler_status = Column(Integer, nullable=False, default=0)
    last_run_time = Column(DateTime)
    next_run_time = Column(DateTime)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'switch_status': self.switch_status,
            'frequency': self.frequency,
            'crawler_status': self.crawler_status,
            'last_run_time': self.last_run_time.isoformat() if self.last_run_time else None,
            'next_run_time': self.next_run_time.isoformat() if self.next_run_time else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
