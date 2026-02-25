from app import db

class Settings(db.Model):
    __tablename__ = 'settings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    
    # Startup
    start_on_boot = db.Column(db.Boolean, default=False)
    minimize_to_tray = db.Column(db.Boolean, default=False)
    
    # Connection
    incoming_port = db.Column(db.Integer, default=6881)
    enable_upnp = db.Column(db.Boolean, default=True)
    proxy_type = db.Column(db.String(20), default='none')
    
    # Bandwidth
    max_download_rate = db.Column(db.Integer, default=0)  # 0 = unlimited
    max_upload_rate = db.Column(db.Integer, default=0)
    
    # Downloads
    download_path = db.Column(db.String(255), default='downloads')
    preallocate_files = db.Column(db.Boolean, default=False)
    append_extension = db.Column(db.Boolean, default=True)
