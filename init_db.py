from app import create_app, db
from app.models.category import Category

app = create_app()

with app.app_context():
    # Créer les tables
    db.create_all()
    
    # Vérifier si les catégories existent déjà
    if Category.query.count() == 0:
        categories = [
            Category(name='Films'),
            Category(name='Séries'),
            Category(name='Musique'),
            Category(name='Logiciels'),
            Category(name='Jeux'),
            Category(name='Livres')
        ]
        
        for cat in categories:
            db.session.add(cat)
        
        db.session.commit()
        print("✅ Base de données initialisée avec succès!")
        print(f"✅ {len(categories)} catégories créées")
    else:
        print("ℹ️  Les catégories existent déjà")
