from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models.torrent import Torrent
from app.models.category import Category
from app.models.user import User

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
    categories = Category.query.all()
    return render_template('index.html', torrents=torrents, categories=categories)

@bp.route('/add', methods=['GET', 'POST'])
def add_torrent():
    if request.method == 'POST':
        torrent_file = request.files.get('torrent_file')
        category_id = request.form.get('category_id')
        
        if torrent_file and torrent_file.filename.endswith('.torrent'):
            from app.utils import parse_torrent_file
            
            file_content = torrent_file.read()
            torrent_info = parse_torrent_file(file_content)
            
            if torrent_info:
                torrent = Torrent(
                    name=torrent_info['name'],
                    hash=torrent_info['hash'],
                    size=torrent_info['size'],
                    category_id=category_id
                )
                db.session.add(torrent)
                db.session.commit()
                flash('Torrent ajouté avec succès!', 'success')
                return redirect(url_for('main.index'))
            else:
                flash('Erreur lors de la lecture du fichier torrent', 'error')
        else:
            flash('Veuillez sélectionner un fichier .torrent', 'error')
    
    categories = Category.query.all()
    return render_template('add_torrent.html', categories=categories)

@bp.route('/torrent/<int:id>')
def torrent_detail(id):
    torrent = Torrent.query.get_or_404(id)
    return render_template('torrent_detail.html', torrent=torrent)

@bp.route('/torrent/<int:id>/pause')
def pause_torrent(id):
    torrent = Torrent.query.get_or_404(id)
    torrent.status = 'paused'
    db.session.commit()
    flash('Torrent mis en pause', 'success')
    return redirect(url_for('main.index'))

@bp.route('/torrent/<int:id>/resume')
def resume_torrent(id):
    torrent = Torrent.query.get_or_404(id)
    torrent.status = 'downloading'
    db.session.commit()
    flash('Torrent repris', 'success')
    return redirect(url_for('main.index'))

@bp.route('/torrent/<int:id>/delete')
def delete_torrent(id):
    torrent = Torrent.query.get_or_404(id)
    db.session.delete(torrent)
    db.session.commit()
    flash('Torrent supprimé', 'success')
    return redirect(url_for('main.index'))

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
