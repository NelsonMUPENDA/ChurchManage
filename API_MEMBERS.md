# API Gestion des Membres - Documentation

## ✅ Fonctionnalités Implémentées

### 1. Backend API (Django REST Framework)

#### Endpoints Membres

| Méthode | Endpoint | Description | Paramètres |
|---------|----------|-------------|------------|
| GET | `/api/members/` | Liste paginée des membres | `page`, `search`, `status`, `gender`, `department` |
| POST | `/api/members/` | Créer un nouveau membre | Corps JSON avec données membre |
| GET | `/api/members/{id}/` | Détails d'un membre | - |
| PATCH | `/api/members/{id}/` | Modifier un membre (partiel) | Corps JSON avec champs à modifier |
| DELETE | `/api/members/{id}/` | Supprimer/Désactiver un membre | `?soft=true` pour soft delete |
| GET | `/api/members/stats/` | Statistiques des membres | - |
| GET | `/api/members/search/` | Recherche avancée | `?q=recherche` |
| GET | `/api/members/print/` | Générer PDF liste | Mêmes filtres que la liste |
| GET | `/api/members/{id}/print_card/` | Carte de membre PDF | - |

#### Endpoints Complémentaires

| Endpoint | Description |
|----------|-------------|
| `/api/families/` | Gestion des familles |
| `/api/home-groups/` | Gestion des groupes de maison |
| `/api/departments/` | Gestion des départements |
| `/api/ministries/` | Gestion des ministères |

### 2. Frontend (members.html)

#### Fonctionnalités UI

- ✅ **Liste des membres** : Affichage en cartes avec photo, nom, email, téléphone
- ✅ **Pagination** : Navigation page par page
- ✅ **Recherche** : En temps réel avec debounce (300ms)
- ✅ **Filtres** : Par statut (actif/inactif/visiteur)
- ✅ **Statistiques** : Total, actifs, nouveaux, mariés
- ✅ **Ajout membre** : Modal avec formulaire complet
- ✅ **Modification** : Modal d'édition avec pré-remplissage
- ✅ **Suppression** : Confirmation + soft delete
- ✅ **Impression liste** : Bouton générant PDF
- ✅ **Carte membre** : PDF individuel par membre
- ✅ **Export** : Prêt pour export Excel
- ✅ **Détail** : Redirection vers page détail

### 3. Sécurité

- Authentification requise (Session + Token)
- Permissions : Admin requis pour modifications
- Filtres automatiques par utilisateur connecté

## 🚀 Utilisation

### Lancer le serveur

```bash
python manage.py runserver
```

### URLs principales

- Application : `http://localhost:8000/`
- API Members : `http://localhost:8000/api/members/`
- Page membres : `http://localhost:8000/members/`

### Exemples de requêtes API

```bash
# Liste avec recherche
curl http://localhost:8000/api/members/?search=jean

# Filtrer par statut
curl http://localhost:8000/api/members/?status=active

# Statistiques
curl http://localhost:8000/api/members/stats/

# Créer un membre
curl -X POST http://localhost:8000/api/members/ \
  -H "Content-Type: application/json" \
  -d '{"user": {"first_name": "Jean", "last_name": "Dupont"}}'
```

## 📁 Fichiers créés/modifiés

```
church_management_app/
├── serializers.py          # ✅ Sérialiseurs DRF
├── api_views.py            # ✅ ViewSets API
├── urls.py                 # ✅ Routes API
└── templates/dashboard/
    └── members.html        # ✅ Interface complète

church_management/
└── settings.py             # ✅ Config DRF

requirements.txt            # ✅ Dépendances
```

## 📊 Modèle Member supporté

Champs disponibles pour création/édition :
- `user` : Informations utilisateur (prénom, nom, email, téléphone, photo)
- `member_number` : Généré automatiquement (CPD-MEM-XXXXXX)
- `post_name`, `birth_date`, `place_of_birth`
- `gender`, `nationality`, `marital_status`
- `occupation`, `public_function`, `church_position`
- `address` : province, city, commune, quarter, avenue, house_number
- `emergency_contact` : nom, téléphone, relation
- `baptism_date`
- `family`, `home_group`, `department`, `ministry`
- `is_active`, `inactive_reason`
