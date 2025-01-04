
# Pamoja NFN Authentication System

## Configuration


```bash
#1. Créer un environnement virtuel :
python3.10 -m venv _venv

#2. Activer l'environnement virtuel :
source _venv/bin/activate           

#3. Installer les dépendances :
pip install -r requirements.txt


#4. Configurer les variables d'environnement :
- Copier `.env.example` vers `.env`
- Remplir les variables requises

#5. Appliquer les migrations :
python manage.py migrate

#6. Créer un superutilisateur :
python manage.py createsuperuser

#7. Lancer le serveur :
python manage.py runserver

#8. Accéder à l'interface d'administration :
http://localhost:8000/admin/

```


## Développement

- Lancer le serveur : `python manage.py runserver`
- Tests : `python manage.py test`
- Shell : `python manage.py shell`

## API Endpoints

### Authentication
- POST `/api/auth/login/` - Connexion
- POST `/api/auth/logout/` - Déconnexion
- POST `/api/auth/token/refresh/` - Rafraîchir le token
- POST `/api/auth/token/revoke/` - Révoquer le token

### Device Management
- GET `/api/auth/devices/` - Liste des appareils
- POST `/api/auth/devices/` - Approuver un appareil
- DELETE `/api/auth/devices/<id>/` - Révoquer un appare
