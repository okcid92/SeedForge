from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    
    with app.app_context():
        from app.routes import main
        app.register_blueprint(main.bp)
        db.create_all()
        
        # Charger les torrents existants
        from app.torrent_manager import torrent_manager
        torrent_manager.load_torrents_from_db()
    
    return app
