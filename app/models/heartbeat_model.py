from config.db import db
from datetime import datetime


class Heartbeat(db.Model):
    __tablename__ = 'heartbeat'

    id = db.Column(db.Integer, primary_key=True)
    caiji_heartbeat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    caiji_status = db.Column(db.SmallInteger, nullable=False, default=0)
    email_heartbeat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    email_status = db.Column(db.SmallInteger, nullable=False, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'caiji_heartbeat': self.caiji_heartbeat.isoformat() if self.caiji_heartbeat else None,
            'caiji_status': self.caiji_status,
            'email_heartbeat': self.email_heartbeat.isoformat() if self.email_heartbeat else None,
            'email_status': self.email_status,
        }

    def __repr__(self):
        return (f"<Heartbeat(id={self.id}, "
                f"caiji_status={self.caiji_status}, email_status={self.email_status})>")
