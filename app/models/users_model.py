from config.db import db
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(100), nullable=False, index=True)
    push_categories = db.Column(JSON, nullable=False, default=list)
    push_switch = db.Column(db.Integer, nullable=False, default=1, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'push_categories': self.push_categories,
            'push_switch': self.push_switch,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"
