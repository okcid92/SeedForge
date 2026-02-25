from app import db
from datetime import datetime

class Statistics(db.Model):
    __tablename__ = 'statistics'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow)
    total_downloaded = db.Column(db.BigInteger, default=0)
    total_uploaded = db.Column(db.BigInteger, default=0)
    
class CompletedTorrent(db.Model):
    __tablename__ = 'completed_torrents'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    size = db.Column(db.BigInteger)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    ratio = db.Column(db.Float, default=0.0)
    download_path = db.Column(db.String(500))
