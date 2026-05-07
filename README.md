# ChurchManageApp - Système de Gestion d'Église

ChurchManageApp est une application de gestion complète pour les églises, développée avec Django. Elle permet de gérer les membres, les finances, les événements, les ministères et bien plus encore, avec un système de permissions granulaire.

## 🚀 Fonctionnalités

- **Tableau de Bord** : Vue d'ensemble des activités de l'église.
- **Gestion des Membres** : Suivi des membres, familles, et groupes de maison.
- **Finances** : Gestion des transactions, catégories financières, et devises (CDF/USD).
- **Événements & Pointage** : Organisation d'événements et suivi des présences (Diaconat).
- **Ministères & Départements** : Organisation structurelle de l'église.
- **Ressources Spirituelles** : Gestion des baptêmes, mariages, évangélisation et formations.
- **Système de Permissions** : Contrôle d'accès granulaire par module et par action.
- **Rapports & Statistiques** : Génération de rapports détaillés sur tous les modules.
- **Mode Sombre/Jour** : Interface adaptative pour un confort d'utilisation optimal.

## 🛠️ Installation

### Prérequis
- Python 3.8+
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le projet**
   ```bash
   git clone https://github.com/NelsonMUPENDA/ChurchManage.git
   cd ChurchManageApp
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv env
   # Sur Windows
   .\env\Scripts\activate
   # Sur Linux/macOS
   source env/bin/activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Appliquer les migrations**
   ```bash
   python manage.py migrate
   ```

5. **Lancer le serveur de développement**
   ```bash
   python manage.py runserver
   ```

L'application sera accessible à l'adresse `http://127.0.0.1:8000`.

## 🔒 Système de Permissions

L'application utilise un système de permissions personnalisé :
- **Modules** : members, families, finances, events, etc.
- **Actions** : view, create, edit, delete, export, print.
- **Middleware** : Un middleware global assure la sécurité des routes.

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
