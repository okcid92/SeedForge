from app import db
from datetime import datetime

class Torrent(db.Model):
    __tablename__ = 'torrents'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    hash = db.Column(db.String(40), unique=True, nullable=False)
    size = db.Column(db.BigInteger)
    seeders = db.Column(db.Integer, default=0)
    leechers = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='downloading')
    progress = db.Column(db.Float, default=0.0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
