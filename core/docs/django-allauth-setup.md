# Guide d'implémentation de Django-Allauth

## Table des matières
1. [Installation](#1-installation)
2. [Configuration de base](#2-configuration-de-base)
3. [Configuration des providers sociaux](#3-configuration-des-providers-sociaux)
4. [Personnalisation des templates](#4-personnalisation-des-templates)
5. [Configuration de l'admin Django](#5-configuration-de-ladmin-django)

## 1. Installation

```bash
pip install django-allauth
pip install "PyJWT<3.0.0"
pip install cryptography
```


## 2. Configuration de base

### Mise à jour de settings.py
Voici les modifications nécessaires à apporter à votre fichier settings.py :

```python
#core/settings.py
INSTALLED_APPS = [
'django.contrib.sites',
'allauth',
'allauth.account',
'allauth.socialaccount',
]


# ... existing code ...

MIDDLEWARE = [
    # Middlewares existants ...
    'allauth.account.middleware.AccountMiddleware',  # Ajouter ce middleware
]



AUTHENTICATION_BACKENDS = [
'django.contrib.auth.backends.ModelBackend',
'allauth.account.auth_backends.AuthenticationBackend'
]
SITE_ID = 1


# Configuration Allauth
# Paramètres de configuration Allauth
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_UNIQUE_EMAIL = True
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Configuration email (développement)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```



### Mise à jour de urls.py
1. Mettre à jour votre fichier urls.py principal (core/urls.py) :

```python
#core/urls.py
urlpatterns = [
    ...
    path('accounts/', include('allauth.urls')),
    ...
]
```

2. Ajouter les URLs de callback dans votre fichier urls.py principal :

```python
#core/urls.py
urlpatterns = [
    ...
    path('accounts/google/login/callback/', views.google_callback, name='google_callback'),
    ...
]
```

3. Créer une vue pour le callback Google :

```python
#core/views.py
def google_callback(request):
    # Logique du callback Google
    pass
```


4. Effectuer les migrations :

```bash
python manage.py migrate
```


5. Créer un site dans l'admin Django (obligatoire pour allauth) :

```bash
python manage.py shell
from django.contrib.sites.models import Site
Site.objects.create(domain='localhost:8000', name='localhost')
```


## 3. Configuration des providers sociaux

### Ajout des providers dans settings.py

```python
INSTALLED_APPS += [
        # ... existing apps ...
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.linkedin_oauth2',
]

# Configuration des providers sociaux
SOCIALACCOUNT_PROVIDERS = {
    'google': {
    'APP': {
        'client_id': config('GOOGLE_CLIENT_ID'),
        'secret': config('GOOGLE_SECRET'),
        'key': ''
        }
    },
    'facebook': {
        'APP': {
        'client_id': config('FACEBOOK_CLIENT_ID'),
        'secret': config('FACEBOOK_SECRET'),
        'key': ''
        }
    },

    'linkedin_oauth2': {
        'APP': {
        'client_id': config('LINKEDIN_CLIENT_ID'),
        'secret': config('LINKEDIN_SECRET'),
        'key': ''
        }
    }
}


# Version complète
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': config('GOOGLE_CLIENT_ID'),
            'secret': config('GOOGLE_SECRET'),
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'facebook': {
        'APP': {
            'client_id': config('FACEBOOK_CLIENT_ID'),
            'secret': config('FACEBOOK_SECRET'),
            'key': ''
        },
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile'],
        'VERSION': 'v15.0'
    },
    'github': {
        'APP': {
            'client_id': config('GITHUB_CLIENT_ID'),
            'secret': config('GITHUB_SECRET'),
            'key': ''
        },
        'SCOPE': [
            'user',
            'repo',
            'read:org',
        ],
    },
    'linkedin_oauth2': {
        'APP': {
            'client_id': config('LINKEDIN_CLIENT_ID'),
            'secret': config('LINKEDIN_SECRET'),
            'key': ''
        },
        'SCOPE': ['r_liteprofile', 'r_emailaddress'],
        'PROFILE_FIELDS': [
            'id',
            'first-name',
            'last-name',
            'email-address',
            'picture-url',
            'public-profile-url',
        ]
    }
}
```

### Configuration du fichier .env
Créez un fichier .env à la racine de votre projet et ajoutez vos clés :
```sh
GOOGLE_CLIENT_ID=votre_client_id
GOOGLE_SECRET=votre_secret

FACEBOOK_CLIENT_ID=votre_client_id
FACEBOOK_SECRET=votre_secret

GITHUB_CLIENT_ID=votre_client_id
GITHUB_SECRET=votre_secret

LINKEDIN_CLIENT_ID=votre_client_id
LINKEDIN_SECRET=votre_secret
```

### Obtenir les clés des providers

- Google : https://console.cloud.google.com/apis/credentials
- Facebook : https://developers.facebook.com/apps/
- GitHub : https://github.com/settings/applications
- LinkedIn : https://www.linkedin.com/developers/apps

#### Google

- Aller sur la `Google Cloud Console` https://console.cloud.google.com/apis/credentials
- Créer une nouvelle clé API
- Sélectionner "OAuth 2.0 Client IDs"
- Choisir "Web application"
- Ajouter les URL de callback (http://localhost:8000/accounts/google/login/callback/ et http://127.0.0.1:8000/accounts/google/login/callback/)
- Copier la clé et la secret

#### Facebook

- Aller sur la `Facebook Developers` https://developers.facebook.com/apps/
- Créer une nouvelle application
- Ajouter les URL de callback (http://localhost:8000/accounts/facebook/login/callback/ et http://127.0.0.1:8000/accounts/facebook/login/callback/)
- Copier la clé et la secret

#### GitHub

- Aller sur la `GitHub Developer Settings` https://github.com/settings/applications
- Créer une nouvelle application
- Ajouter les URL de callback (http://localhost:8000/accounts/github/login/callback/ et http://127.0.0.1:8000/accounts/github/login/callback/)
- Copier la clé et la secret


#### LinkedIn

- Aller sur la `LinkedIn Developer Settings` https://www.linkedin.com/developers/apps
- Créer une nouvelle application
- Ajouter les URL de callback (http://localhost:8000/accounts/linkedin/login/callback/ et http://127.0.0.1:8000/accounts/linkedin/login/callback/)
- Copier la clé et la secret





Les principales fonctionnalités ajoutées :
- Authentification par email
- Vérification d'email
- Réinitialisation de mot de passe
- Possibilité d'ajouter des providers sociaux (Google, Facebook, etc.)



## 4. Personnalisation des templates

Pour personnaliser les templates d'authentification, créez un dossier templates/account/ dans votre projet et copiez les templates de base d'allauth que vous souhaitez modifier.


Ces templates incluent :
- Design responsive avec Bootstrap
- Intégration des boutons de connexion sociale
- Gestion des erreurs de formulaire
- Messages de validation
- Navigation entre connexion et inscription
- Support multilingue avec {% trans %}


**Créer la structure des dossiers :**

```sh
mkdir -p templates/account
mkdir -p templates/socialaccount
```

**Créer le fichier email.html :**

```sh
templates/account/email.html
```

### Templates principaux à personnaliser :
- login.html
- signup.html
- logout.html
- email.html
- confirm_email_verification_code.html
- account_inactive.html
- account_confirm_email.html
- account_email_verification_sent.html
- account_email_verification_done.html
- account_email_verification_invalid.html
- account_email_verification_done.html

### Ajout des styles CSS

```css
/* static/css/main.css */


/* Style pour les boutons sociaux */
.btn-linkedin {
background-color: #0077b5;
color: white;
}
.btn-linkedin:hover {
background-color: #006399;
color: white;
}
/* Séparateur avec texte */
.separator {
display: flex;
align-items: center;
text-align: center;
margin: 20px 0;
}
.separator::before,
.separator::after {
content: '';
flex: 1;
border-bottom: 1px solid #dee2e6;
}
.separator span {
padding: 0 10px;
color: #6c757d;
background: #fff;
}

```


## 5. Configuration de l'admin Django

1. Créer un superutilisateur :
```bash
python manage.py createsuperuser
```

2. Lancer le serveur :
```bash
python manage.py runserver
```

2. Configurer le site dans l'admin Django :
   - Accéder à http://localhost:8000/admin
   - Aller dans "Sites"
   - Modifier le site existant ou en créer un nouveau :
     - Domain name: localhost:8000
     - Display name: localhost

3. Configurer les applications sociales :
   - Aller dans "Social Applications"
   - Pour chaque provider (Google, Facebook, GitHub, LinkedIn) :
     - Choisir le provider
     - Donner un nom
     - Entrer le Client ID
     - Entrer la Secret Key
     - Sélectionner le site dans "Available sites"

## URLs de callback à configurer

### Google

https://accounts.google.com/o/oauth2/auth

http://localhost:8000/accounts/google/login/callback/
http://127.0.0.1:8000/accounts/google/login/callback/



