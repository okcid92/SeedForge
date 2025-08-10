## 💡 **Règles Git/GitHub** *(à appliquer tout le long du projet)*

- Toujours travailler sur **une branche dédiée par fonctionnalité**.
- **Commit régulier** (toutes les 2-3 étapes max).
- Push sur **GitHub privé** après chaque commit.
- À chaque début de phase → créer une nouvelle branche.
- Fusionner sur `main` une fois les tests validés.

---

### **Phase 1 — Bases Python & Git Ready (J1 → J2)**

🎯 Objectif : Comprendre Python de base et mettre en place Git/GitHub privé

---

**Jour 1 : Syntaxe & Structures de base**

- Variables, types (int, float, str, list, dict)
- Boucles (for, while)
- Conditions (if, elif, else)
- Fonctions (déclaration, paramètres, valeurs de retour)
- **Exercice** : Script qui trie une liste de nombres

**Git/GitHub privé** *(Palier 1)* :

1. Installer et configurer Git ([user.name](https://user.name/), [user.email](https://user.email/))
2. Créer un repo **privé** sur GitHub
3. Lier le repo local au distant (`git remote add origin …`)
4. Faire le premier commit et push sur GitHub

---

**Jour 2 : Modules, Fichiers & Exceptions**

- Importation (`import`, `from … import`)
- Lire/écrire fichiers (`open`, `with`)
- Gestion des erreurs (`try/except`)
- List comprehensions
- **Exercice** : Script qui lit un `.txt` et compte les mots

**Git/GitHub privé** :

- Commit + push des modifications

---

### **Phase 2 — Bases Flask (J3 → J8)**

🎯 Objectif : Comprendre et structurer un projet Flask

---

**Jour 3 : Introduction à Flask** *(Palier 2 — Objectif 7)*

- Installer Flask
- Créer un Hello World
- Comprendre `app.route` et [app.run](https://app.run/)
- **Exercice** : Route `/bonjour` affichant ton prénom
- **Git/GitHub privé** : Nouvelle branche `flask-learning` + push

---

**Jour 4 : Templates & HTML** *(Palier 2 — Objectifs 9 & 10)*

- Utiliser Jinja2 (`{{ variable }}`, `{% for ... %}`)
- Organisation du dossier `templates/`
- **Exercice** : Page HTML listant des films
- **Git** : Commit + push

---

**Jour 5 : Formulaires & POST** *(Palier 3 — Objectifs 12 & 13)*

- `request.form`, GET vs POST
- Redirections après action (`redirect(url_for())`)
- **Exercice** : Formulaire pseudo → affichage
- **Git** : Commit + push

---

**Jour 6 : Base de données MySQL** *(Palier 4 — Objectifs 19 & 20)*

- Installation & connexion MySQL
- Créer table simple
- **Exercice** : Route `/utilisateurs` qui lit la BDD
- **Git** : Commit + push

---

**Jour 7 : Organisation du projet Flask** *(Palier 6 — Objectif 24)*

- Structure MVC (`app/`, `templates/`, `static/`)
- Fichier [config.py](https://config.py/)
- **Exercice** : Réorganisation du code
- **Git** : Commit + push

---

**Jour 8 : CRUD SQL complet** *(Palier 4 — Objectifs 15 → 18)*

- INSERT, SELECT, UPDATE, DELETE
- **Exercice** : Mini CRUD utilisateurs
- **Git** : Commit + push

---

### **Phase 3 — Conception Gestionnaire de Torrents (J9 → J12)**

🎯 Objectif : Planification & préparation

---

**Jour 9 : Analyse du projet**

- Définir fonctionnalités (ajout torrent, suivi seeds/peers, catégories)
- Pages prévues
- **Git** : Nouvelle branche `project-setup` + push

---

**Jour 10 : Arborescence projet** *(Palier 6 — Objectif 24)*

- Créer l’architecture complète (`app/`, [config.py](https://config.py/), etc.)
- **Git** : Commit + push

---

**Jour 11 : Config BDD + Modèles** *(Palier 4 — Objectif 19)*

- Tables MySQL : `users`, `torrents`, `categories`
- Script SQL création
- **Git** : Commit + push

---

**Jour 12 : API Torrent**

- Choix lib (`libtorrent`, `qbittorrent-api`)
- Test ajout torrent
- **Git** : Commit + push

---

### **Phase 4 — Développement du Projet (J13 → J28)**

🎯 Objectif : Construire le gestionnaire de torrents

---

- **J13 → J14** : Page accueil + liste torrents *(Git : Commit + push)*
- **J15 → J16** : Formulaire ajout torrent *(Git : Commit + push)*
- **J17 → J18** : Page détails torrent (seeders, taille, statut) *(Git : Commit + push)*
- **J19 → J20** : Catégorisation torrents *(Git : Commit + push)*
- **J21 → J22** : Authentification utilisateurs *(Git : Commit + push)*
- **J23 → J24** : Téléchargement direct *(Git : Commit + push)*
- **J25 → J26** : Gestion erreurs/logs *(Git : Commit + push)*
- **J27 → J28** : Design CSS + responsive *(Palier 5 — Objectif 21)* *(Git : Commit + push)*

---

### **Phase 5 — Tests, Debug & Déploiement (J29 → J40)**

🎯 Objectif : Finaliser et publier

---

- **J29 → J31** : Tests unitaires *(Pytest)* *(Git : Commit + push)*
- **J32 → J34** : Correction bugs *(Git : Commit + push)*
- **J35 → J37** : Préparer déploiement *(Gunicorn + Nginx ou Render)* *(Git : Commit + push)*
- **J38** : Déploiement en ligne
- **J39 → J40** : Rédaction README complet + vidéo démo *(Palier 6 — Objectif 25 & 27)* *(Git : Commit + push)*

---

🔥 **Bonus Versioning Pro** *(à appliquer tout du long)* :

- Chaque fonctionnalité = **branche dédiée**
- Simuler des **pull requests**
- Commits **clairs et structurés** :
  - `feature: ajout du formulaire de tâches`
  - `fix: correction du bug de suppression`
  - `refactor: réorganisation des fichiers CSS`

CHECKLIST

| Jour | Objectif principal | Détails & Actions |
| --- | --- | --- |
|[] 1 | Installation & Setup | Installer Python 3.13.6, WSL, VS Code, Git. Créer un environnement virtuel. |
| 2 | Bases Python | Révisions variables, boucles, fonctions. Exercices simples. |
| 3 | Bases Python | Manipulation fichiers, JSON, datetime, modules. |
| 4 | Git/GitHub | Apprendre commandes Git, créer repo, commit/push. |
| 5 | Découverte Flask | Installation Flask, Hello World, routes simples. |
| 6 | Flask routes avancées | GET/POST, paramètres URL, redirect, templates simples. |
| 7 | Jinja2 | Variables, boucles, conditions dans templates. |
| 8 | HTML/CSS rapide | Créer un template de base avec style simple. |
| 9 | Forms & Flask-WTF | Créer formulaire, valider données, gérer erreurs. |
| 10 | Bases BDD SQL | Tables, SELECT, INSERT, UPDATE, DELETE. |
| 11 | SQLAlchemy | Connexion DB, modèles, migrations. |
| 12 | CRUD Flask | Créer/afficher/modifier/supprimer données avec Flask + SQLAlchemy. |
| 13 | Authentification | Créer login/logout, sessions, gestion utilisateurs. |
| 14 | Téléversement fichiers | Upload fichier, restrictions taille/format. |
| 15 | Structure projet Flask | Blueprints, organisation code. |
| 16 | Flask avancé | Pagination, messages flash, erreurs 404/500 custom. |
| 17 | API Flask | Créer API JSON avec Flask (Flask-RESTful ou jsonify). |
| 18 | Consommer API | Faire requêtes API avec Python (requests). |
| 19 | Sécurité | Hashing mots de passe, CSRF, validation. |
| 20 | 📌 Pause / révisions | Revoir tout le code et concepts vus. |
| 21 | Projet – Base | Créer repo projet (gestionnaire torrent), préparer structure. |
| 22 | Page accueil | Afficher liste des torrents (mock data). |
| 23 | Page ajout torrent | Formulaire ajout (upload fichier torrent ou URL). |
| 24 | Intégration backend | Connecter ajout torrent au code Python. |
| 25 | Affichage détails | Voir seeders, leechers, statut téléchargement. |
| 26 | Gestion téléchargement | Lancer/stopper torrents (lib torrent). |
| 27 | Classement torrents | Par type (films, musique, séries…). |
| 28 | Authentification projet | Login/logout utilisateurs projet. |
| 29 | Interface responsive | Adapter HTML/CSS, un peu de JS. |
| 30 | API projet | Exposer endpoints pour torrents. |
| 31 | Tests unitaires | pytest, tester routes et fonctions clés. |
| 32 | Déploiement local | Tester avec Flask en mode prod (gunicorn). |
| 33 | Déploiement serveur | Mettre sur VPS/WSL avec nginx. |
| 34 | Monitoring | Logs, gestion erreurs, uptime. |
| 35 | Optimisations | Perf DB, cache, compression fichiers. |
| 36 | Améliorations UI | Ajustements design. |
| 37 | Documentation | Rédiger README clair, instructions installation. |
| 38 | Derniers tests | Vérification fonctionnalités principales. |
| 39 | Démo finale | Présenter projet, tester devant quelqu’un. |
| 40 | 📌 Bilan | Analyser ce qui a marché, noter points à améliorer. |
