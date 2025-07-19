# Application Streamlit + FastAPI

Une application complète avec un backend FastAPI et un frontend Streamlit, prête pour le déploiement sur Google Cloud Platform.

# Déploiement simple (identique)

chmod +x deploy.sh

./deploy.sh

# test en local du docker compose :

- http://localhost:8501
- http://localhost:8000

## 🏗️ Architecture

```
gcp_vm_repo/
├── backend/
│   ├── Dockerfile
│   ├── server.py          # API FastAPI avec SQLAlchemy
│   ├── database.py        # Configuration DB (optionnel)
│   └── requirements.txt
├── frontend/
│   ├── Dockerfile
│   ├── main.py           # Interface Streamlit
│   └── requirements.txt
├── docker-compose.yml    # Inclut PostgreSQL
├── deploy.sh
├── .gitignore
└── README.md
```

## ✨ Fonctionnalités

### Backend (FastAPI)
- ✅ API RESTful complète avec CRUD
- ✅ Base de données PostgreSQL avec SQLAlchemy ORM
- ✅ Migrations automatiques des tables
- ✅ Données de test pré-configurées
- ✅ Documentation automatique avec Swagger
- ✅ Validation des données avec Pydantic
- ✅ Support CORS pour le frontend
- ✅ Health check endpoint

### Frontend (Streamlit)
- ✅ Interface utilisateur moderne et responsive
- ✅ Formulaires interactifs pour la gestion des données
- ✅ Visualisations avec graphiques
- ✅ Statistiques en temps réel
- ✅ Gestion des erreurs et état de connexion API
- ✅ Design moderne avec émojis et couleurs

## 🚀 Déploiement Rapide sur GCP

### 1. Prérequis
- Une VM Google Cloud Platform avec Ubuntu 20.04+
- Accès SSH à la VM
- Ports 8000, 8501 et 5432 ouverts dans le firewall
- Au moins 2GB de RAM (recommandé pour PostgreSQL)

### 2. Déploiement automatique

```bash
# Cloner le repository
git clone <votre-repo>
cd gcp_vm_repo

# Rendre le script exécutable
chmod +x deploy.sh

# Exécuter le déploiement
./deploy.sh
```

Le script `deploy.sh` va automatiquement :
- Installer Docker et Docker Compose si nécessaire
- Démarrer PostgreSQL dans un conteneur
- Construire les images Docker
- Initialiser la base de données avec des données de test
- Démarrer les conteneurs
- Configurer le firewall
- Tester la connectivité

### 3. Accès aux services

Après le déploiement :
- **Frontend Streamlit** : `http://[IP_VM]:8501`
- **API FastAPI** : `http://[IP_VM]:8000`  
- **Documentation API** : `http://[IP_VM]:8000/docs`

## 🛠️ Développement Local

### Avec Docker Compose (Recommandé)

```bash
# Démarrer tous les services
docker-compose up --build

# En mode détaché
docker-compose up --build -d

# Voir les logs
docker-compose logs -f

# Arrêter les services
docker-compose down
```

### Développement manuel

**Backend :**
```bash
cd backend
pip install -r requirements.txt
# Démarrer PostgreSQL localement ou modifier DATABASE_URL
export DATABASE_URL=postgresql://user:password@localhost:5432/appdb
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

**Frontend :**
```bash
cd frontend
pip install -r requirements.txt
export API_URL=http://localhost:8000
streamlit run main.py
```

## 📊 API Endpoints

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Message de bienvenue |
| GET | `/health` | Health check |
| GET | `/items` | Lister tous les items |
| GET | `/items/{id}` | Récupérer un item |
| POST | `/items` | Créer un item |
| PUT | `/items/{id}` | Modifier un item |
| DELETE | `/items/{id}` | Supprimer un item |

## 🔧 Configuration

### Variables d'environnement

**Frontend :**
- `API_URL` : URL du backend (défaut: `http://localhost:8000`)

**Backend :**
- `DATABASE_URL` : URL de connexion PostgreSQL (défaut: `postgresql://user:password@db:5432/appdb`)

### Base de données

La base de données PostgreSQL est automatiquement configurée avec :
- **Utilisateur** : `user`
- **Mot de passe** : `password` 
- **Base de données** : `appdb`
- **Port** : 5432

Les données sont persistées dans un volume Docker `postgres_data`.

### Ports
- **Backend** : 8000
- **Frontend** : 8501
- **PostgreSQL** : 5432

## 🔒 Sécurité pour la Production

Pour un déploiement en production, considérez :

1. **CORS** : Modifier `allow_origins=["*"]` dans `server.py`
2. **HTTPS** : Utiliser un reverse proxy (Nginx) avec certificats SSL
3. **Base de données** : Sécuriser PostgreSQL (mots de passe forts, SSL)
4. **Authentification** : Ajouter un système d'auth JWT
5. **Logs** : Configurer un système de logging approprié
6. **Monitoring** : Ajouter des métriques et monitoring
7. **Backup** : Configurer des sauvegardes automatiques de la DB

## 📝 Logs et Debugging

```bash
# Voir les logs en temps réel
docker-compose logs -f

# Logs d'un service spécifique
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db

# Accéder au conteneur
docker-compose exec backend bash
docker-compose exec frontend bash
docker-compose exec db psql -U user -d appdb

# Redémarrer un service
docker-compose restart backend
```

## 🔄 Mise à jour

```bash
# Reconstruire après des modifications
docker-compose up --build

# Forcer la reconstruction
docker-compose build --no-cache
docker-compose up
```

## 📞 Support

En cas de problème :
1. Vérifiez les logs : `docker-compose logs`
2. Testez la connectivité : `curl http://localhost:8000/health`
3. Vérifiez l'état des conteneurs : `docker-compose ps`

## 🎯 Prochaines étapes

- [x] ~~Ajouter une vraie base de données~~ ✅ PostgreSQL intégré
- [ ] Implémenter l'authentification
- [ ] Ajouter des tests automatisés  
- [ ] Configurer CI/CD
- [ ] Monitoring et métriques
- [ ] Système de backup automatique
- [ ] Migration vers un cluster Kubernetes


# gcp_vm
Public project to be hosted on a GCP Virtual Machine.

## Stack 

- FastAPI
- Streamlit
- Docker
- Google Cloud Platform (Compute Engine)
- Github

## VM parameters

- Accessible via ssh
- Ports 8000, 8501 et 5432 ouverts dans le firewall

OS : Ubuntu 24.04
Disk size :
CPU :
RAM CPU : 
GPU : X
RAM GPU : X


## Building images & pushing them to Google Artifact Registry 




## Once connected to the VM itself 

1) git clone
2) docker compose up --build


## GCP VM

Frontend link (port : 8051 => http://localhost:8501) : http://[IP_VM]:8501

Backend link (swagger UI, port : 8000 => http://localhost:8000 puis http://backend:8000) : http://[IP_VM]:8000 (/docs)



