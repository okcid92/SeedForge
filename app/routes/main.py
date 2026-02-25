from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app import db
from app.models.torrent import Torrent
from app.models.category import Category
from app.models.user import User
from app.torrent_manager import torrent_manager
from app.search_engine import search_engine
import os

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    category_id = request.args.get('category')
    search = request.args.get('q')
    
    query = Torrent.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    if search:
        query = query.filter(Torrent.name.contains(search))
    
    torrents = query.all()
    
    # Mettre à jour les statuts depuis libtorrent
    for torrent in torrents:
        status = torrent_manager.get_status(torrent.hash)
        if status:
            torrent.progress = status['progress'] / 100
            torrent.seeders = status['num_seeds']
            torrent.leechers = status['num_peers']
    
    categories = Category.query.all()
    return render_template('index.html', torrents=torrents, categories=categories)

@bp.route('/add', methods=['GET', 'POST'])
def add_torrent():
    if request.method == 'POST':
        torrent_file = request.files.get('torrent_file')
        magnet_link = request.form.get('magnet_link')
        category_id = request.form.get('category_id')
        
        if torrent_file and torrent_file.filename.endswith('.torrent'):
            from app.utils import parse_torrent_file
            
            file_content = torrent_file.read()
            torrent_info = parse_torrent_file(file_content)
            
            if torrent_info:
                # Sauvegarder le fichier
                upload_path = os.path.join('uploads', torrent_file.filename)
                with open(upload_path, 'wb') as f:
                    f.write(file_content)
                
                # Ajouter au gestionnaire
                torrent_manager.add_torrent(upload_path, torrent_info['hash'])
                
                torrent = Torrent(
                    name=torrent_info['name'],
                    hash=torrent_info['hash'],
                    size=torrent_info['size'],
                    category_id=category_id,
                    status='downloading'
                )
                db.session.add(torrent)
                db.session.commit()
                flash('Torrent ajouté et téléchargement démarré!', 'success')
                return redirect(url_for('main.index'))
            else:
                flash('Erreur lors de la lecture du fichier torrent', 'error')
        
        elif magnet_link:
            # Extraire le hash du magnet link
            import re
            match = re.search(r'btih:([a-fA-F0-9]{40})', magnet_link)
            if match:
                torrent_hash = match.group(1).lower()
                
                # Ajouter au gestionnaire
                torrent_manager.add_magnet(magnet_link, torrent_hash)
                
                torrent = Torrent(
                    name='Magnet Link',
                    hash=torrent_hash,
                    size=0,
                    category_id=category_id,
                    status='downloading'
                )
                db.session.add(torrent)
                db.session.commit()
                flash('Magnet link ajouté!', 'success')
                return redirect(url_for('main.index'))
            else:
                flash('Magnet link invalide', 'error')
        else:
            flash('Veuillez sélectionner un fichier .torrent ou entrer un magnet link', 'error')
    
    categories = Category.query.all()
    return render_template('add_torrent.html', categories=categories)

@bp.route('/torrent/<int:id>')
def torrent_detail(id):
    torrent = Torrent.query.get_or_404(id)
    status = torrent_manager.get_status(torrent.hash)
    
    if status:
        torrent.progress = status['progress'] / 100
        torrent.seeders = status['num_seeds']
        torrent.leechers = status['num_peers']
        
        # Mettre à jour le statut dans la DB si nécessaire
        current_status = torrent.status
        new_status = current_status

        if status['state'] == 'seeding' or status['state'] == 'finished':
            new_status = 'completed'
        elif status['state'] == 'paused':
            new_status = 'paused'
        elif status['state'] == 'downloading':
            new_status = 'downloading'
        
        if new_status != current_status:
            torrent.status = new_status
            db.session.commit()
            
    return render_template('torrent_detail.html', torrent=torrent, status=status)

@bp.route('/torrent/<int:id>/pause')
def pause_torrent(id):
    torrent = Torrent.query.get_or_404(id)
    torrent_manager.pause_torrent(torrent.hash)
    torrent.status = 'paused'
    db.session.commit()
    flash('Torrent mis en pause', 'success')
    return redirect(url_for('main.index'))

@bp.route('/torrent/<int:id>/resume')
def resume_torrent(id):
    torrent = Torrent.query.get_or_404(id)
    torrent_manager.resume_torrent(torrent.hash)
    torrent.status = 'downloading'
    db.session.commit()
    flash('Torrent repris', 'success')
    return redirect(url_for('main.index'))

@bp.route('/torrent/<int:id>/delete')
def delete_torrent(id):
    torrent = Torrent.query.get_or_404(id)
    torrent_manager.remove_torrent(torrent.hash, delete_files=True)
    db.session.delete(torrent)
    db.session.commit()
    flash('Torrent supprimé', 'success')
    return redirect(url_for('main.index'))

@bp.route('/api/torrent/<int:id>/status')
def torrent_status_api(id):
    torrent = Torrent.query.get_or_404(id)
    status = torrent_manager.get_status(torrent.hash)
    return jsonify(status if status else {})

@bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Connectez-vous pour accéder au tableau de bord', 'error')
        return redirect(url_for('main.login'))
    
    total = Torrent.query.count()
    active = Torrent.query.filter_by(status='downloading').count()
    completed = Torrent.query.filter_by(status='completed').count()
    paused = Torrent.query.filter_by(status='paused').count()
    
    return render_template('dashboard.html', total=total, active=active, completed=completed, paused=paused)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Nom d\'utilisateur déjà pris', 'error')
            return redirect(url_for('main.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email déjà utilisé', 'error')
            return redirect(url_for('main.register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Inscription réussie! Connectez-vous', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Connexion réussie!', 'success')
            return redirect(url_for('main.dashboard'))
        flash('Identifiants incorrects', 'error')
    
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Déconnexion réussie', 'success')
    return redirect(url_for('main.index'))

@bp.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'user_id' not in session:
        flash('Connectez-vous pour accéder aux paramètres', 'error')
        return redirect(url_for('main.login'))
    
    from app.models.settings import Settings
    user_settings = Settings.query.filter_by(user_id=session['user_id']).first()
    
    if not user_settings:
        user_settings = Settings(user_id=session['user_id'])
        db.session.add(user_settings)
        db.session.commit()
    
    if request.method == 'POST':
        user_settings.start_on_boot = 'start_on_boot' in request.form
        user_settings.minimize_to_tray = 'minimize_to_tray' in request.form
        user_settings.incoming_port = int(request.form.get('incoming_port', 6881))
        user_settings.enable_upnp = 'enable_upnp' in request.form
        user_settings.max_download_rate = int(request.form.get('max_download_rate', 0))
        user_settings.max_upload_rate = int(request.form.get('max_upload_rate', 0))
        user_settings.download_path = request.form.get('download_path', 'downloads')
        user_settings.preallocate_files = 'preallocate_files' in request.form
        
        db.session.commit()
        flash('Paramètres sauvegardés!', 'success')
        return redirect(url_for('main.settings'))
    
    return render_template('settings.html', settings=user_settings)

@bp.route('/statistics')
def statistics():
    from app.models.statistics import Statistics, CompletedTorrent
    
    # Stats globales
    total_downloaded = db.session.query(db.func.sum(Statistics.total_downloaded)).scalar() or 0
    total_uploaded = db.session.query(db.func.sum(Statistics.total_uploaded)).scalar() or 0
    ratio = (total_uploaded / total_downloaded) if total_downloaded > 0 else 0
    
    # Derniers 7 jours
    from datetime import datetime, timedelta
    week_ago = datetime.utcnow() - timedelta(days=7)
    daily_stats = Statistics.query.filter(Statistics.date >= week_ago).order_by(Statistics.date).all()
    
    # Torrents terminés
    completed = CompletedTorrent.query.order_by(CompletedTorrent.completed_at.desc()).limit(10).all()
    
    return render_template('statistics.html', 
                         total_downloaded=total_downloaded,
                         total_uploaded=total_uploaded,
                         ratio=ratio,
                         daily_stats=daily_stats,
                         completed=completed)

@bp.route('/search-torrents')
def search_torrents():
    return render_template('search_torrents.html')

@bp.route('/api/search', methods=['POST'])
def api_search():
    query = request.json.get('query', '')
    if not query:
        return jsonify({'results': []})
    
    results = search_engine.search_all(query, limit=30)
    return jsonify({'results': results})

@bp.route('/add-from-search', methods=['POST'])
def add_from_search():
    magnet = request.form.get('magnet')
    name = request.form.get('name')
    size = request.form.get('size')
    category_id = request.form.get('category_id', 1)
    
    if magnet:
        import re
        match = re.search(r'btih:([a-fA-F0-9]{40})', magnet)
        if match:
            torrent_hash = match.group(1).lower()
            
            torrent_manager.add_magnet(magnet, torrent_hash)
            
            torrent = Torrent(
                name=name,
                hash=torrent_hash,
                size=0,
                category_id=category_id,
                status='downloading'
            )
            db.session.add(torrent)
            db.session.commit()
            flash('Torrent ajouté depuis la recherche!', 'success')
            return redirect(url_for('main.index'))
    
    flash('Erreur lors de l\'ajout', 'error')
    return redirect(url_for('main.search_torrents'))
