# 🌱 SeedForge - Fonctionnalités

## 🎯 Fonctionnalités Principales

### 1. Gestion des Torrents
- ✅ Ajouter un torrent (fichier .torrent ou magnet link)
- ✅ Lister tous les torrents avec statut en temps réel
- ✅ Voir les détails d'un torrent (seeders, leechers, taille, progression)
- ⚡ Pause/Reprise des téléchargements
- ⚡ Supprimer un torrent
- ⚡ Définir la priorité de téléchargement (haute, normale, basse)

### 2. Catégorisation
- ✅ Catégories prédéfinies (Films, Séries, Musique, Logiciels, Jeux, Livres)
- ⚡ Filtrer les torrents par catégorie
- ⚡ Recherche de torrents par nom

### 3. Authentification & Utilisateurs
- ✅ Inscription/Connexion/Déconnexion
- ⚡ Profil utilisateur avec statistiques
- ⚡ Historique des téléchargements par utilisateur
- ⚡ Ratio upload/download

### 4. Tableau de Bord
- ⚡ Vue d'ensemble : torrents actifs, vitesse download/upload
- ⚡ Graphiques de bande passante
- ⚡ Espace disque disponible
- ⚡ Notifications pour torrents terminés

### 5. Paramètres & Configuration
- ⚡ Limiter la vitesse de téléchargement/upload
- ⚡ Choisir le dossier de destination
- ⚡ Planifier les téléchargements (heures creuses)
- ⚡ Mode sombre/clair

### 6. Fonctionnalités Avancées
- ⚡ Lecteur vidéo intégré (streaming pendant le téléchargement)
- ⚡ Extraction automatique des archives (.zip, .rar)
- ⚡ Notifications push/email
- ⚡ API REST pour contrôle externe
- ⚡ Support multi-utilisateurs avec permissions

### 7. Sécurité
- ✅ Hashing des mots de passe
- ⚡ Protection CSRF
- ⚡ Limitation des tentatives de connexion
- ⚡ Logs d'activité

## 📊 Priorités d'Implémentation

### Phase 1 - MVP (Minimum Viable Product)
1. Pause/Reprise/Suppression des torrents
2. Filtrage par catégorie
3. Recherche de torrents
4. Inscription utilisateur

### Phase 2 - Amélioration UX
5. Tableau de bord avec statistiques
6. Profil utilisateur
7. Paramètres de vitesse

### Phase 3 - Fonctionnalités Avancées
8. Lecteur vidéo intégré
9. API REST
10. Notifications

## 🚀 Fonctionnalités à Implémenter Maintenant

### A. Contrôle des Torrents (Pause/Reprise/Suppression)
- Route `/torrent/<id>/pause` - Mettre en pause
- Route `/torrent/<id>/resume` - Reprendre
- Route `/torrent/<id>/delete` - Supprimer

### B. Filtrage et Recherche
- Route `/category/<id>` - Filtrer par catégorie
- Route `/search?q=<query>` - Rechercher

### C. Inscription Utilisateur
- Route `/register` - Formulaire d'inscription
- Validation email unique

### D. Tableau de Bord
- Route `/dashboard` - Vue d'ensemble
- Statistiques : total torrents, actifs, terminés
- Vitesse moyenne download/upload
