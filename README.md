# pamoja-nfn.com
Pamoja - L'annuaire Afro des prestataires valorisant la diversité afrodescendante 


## Contexte et Objectifs  
L'annuaire Afro vise à recenser et mettre en avant des prestataires et adresses valorisant la diversité afrodescendante dans divers secteurs d'activités (alimentation, mode, culture, etc.).  
Après une première version en format Excel, nous souhaitons migrer vers une **Web App interactive** offrant :  
- Une meilleure expérience utilisateur.  
- Une gestion optimisée des informations.  

### Objectifs de la Web App :  
- Fournir une plateforme facile à utiliser.  
- Permettre une gestion efficace des contenus et mises à jour.



```sh
pamoja/
├── messaging/          # Gestion des messages
├── listing/           # Gestion des annonces
├── users/             # Gestion des utilisateurs
├── favorites/         # ⭐ Nouvelle app pour les favoris
└── search/            # 🔍 Nouvelle app pour la recherche
```


Dans notre application, la séparation est préférable car :
1. `Séparation des responsabilités` : Chaque app a un rôle spécifique
2. `Réutilisabilité` : Ces fonctionnalités peuvent être utilisées par différentes apps
3. `Maintenance` : Plus facile à maintenir et tester
4. `Scalabilité` : Plus facile à faire évoluer indépendamment

**Par exemple :**
- `favorites` peut être utilisé pour favoriser des listings, des profils, etc.
- `search` peut indexer et rechercher dans les listings, les profils, les messages, etc.

Voulez-vous que je détaille la structure complète d'une de ces nouvelles apps ?



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
python manage.py makemigrations
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




## Diagramme Entité-Relation (ERD) - Utilisateur et Profil

### Utilisateur

- **Champs** :
  - `id` : Clé primaire
  - `username` : Nom d'utilisateur (unique, indexé)
  - `email` : Adresse email (unique, indexé)
  - `password` : Mot de passe (hashé)
  - `role` : Rôle (choix : Simple utilisateur, Prestataire, Administrateur, Modérateur, Staff, etc.)
  - `date_joined` : Date d'inscription
  - `is_active` : Statut actif/inactif
  - `is_staff` : Permission pour accéder à l'interface d'administration
- **Relations** :
  - Chaque utilisateur peut avoir un seul `Profil`.

---

### Profil

- **Champs** :
  - `id` : Clé primaire
  - `user` : Clé étrangère vers `Utilisateur` (OneToOneField)
  - `description` : Description du profil
  - `contact_info` : Coordonnées (téléphone, email)
  - `profile_image` : URL de l'image (hébergée sur Cloudinary ou Amazon S3)
  - `date_registered` : Date d'enregistrement
  - `verified` : Statut de vérification du profil (booléen)
  - `verification_date` : Date de vérification
  - `verified_by` : Administrateur ayant vérifié le profil (clé étrangère vers `Utilisateur`)
  - `social_media_links` : Liens vers les réseaux sociaux (JSONField)
- **Relations** :
  - Peut être associé à un ou plusieurs `Listings`
  - Associé à plusieurs `Language` (ManyToManyField)

### Language

- **Champs** :
  - `id` : Clé primaire
  - `name` : Nom de la langue (unique)
  - `code` : Code ISO 639-1 de la langue (2 caractères, unique)
- **Relations** :
  - Peut être associé à plusieurs `Profils`

### SocialMediaPlatform

- **Champs** :
  - `id` : Clé primaire
  - `name` : Nom de la plateforme (unique)
  - `base_url` : URL de base de la plateforme
  - `icon` : Classe d'icône pour l'affichage
- **Relations** :
  - Utilisé comme référence pour les `social_media_links` des `Profils`

---

## Listing

- **Champs** :
  - `id` : Clé primaire
  - `profile` : Clé étrangère vers `Profil`
  - `category` : Clé étrangère vers `Catégorie`
  - `subcategory` : Clé étrangère vers `SousCatégorie`
  - `type` : Type de listing (choix : Individuel, Entreprise)
  - `company_name` : Nom de l'entreprise (uniquement si type=Entreprise)
  - `description` : Description du listing
  - `location` : Localisation (ville, région, pays)
  - `contact_info` : Coordonnées spécifiques au listing
  - `logo` : URL du logo ou image du listing
  - `date_created` : Date de création
  - `website_url` : Site web du prestataire (URLField, optionnel)
  - `business_hours` : Horaires d'ouverture (JSONField)
  - `status` : État du listing (choix : Actif, Inactif, En attente de validation)
  - `average_rating` : Note moyenne calculée (DecimalField)
- **Relations** :
  - Relié à une seule `Catégorie` et éventuellement à une `SousCatégorie`
  - Associé à plusieurs `Tag` (ManyToManyField)

### Tag

- **Champs** :
  - `id` : Clé primaire
  - `name` : Nom du tag (unique)
  - `slug` : Version URL-friendly du nom
  - `category` : Catégorie du tag (optionnel, ForeignKey vers `Catégorie`)
- **Relations** :
  - Peut être associé à plusieurs `Listings`
  - Peut être associé à une `Catégorie`

---

### Catégorie

- **Champs** :
  - `id` : Clé primaire
  - `name` : Nom de la catégorie (unique)
  - `description` : Description de la catégorie
- **Relations** :
  - Contient plusieurs `SousCatégories`.
  - Contient plusieurs `Listings`.

---

### SousCatégorie

- **Champs** :
  - `id` : Clé primaire
  - `category` : Clé étrangère vers `Catégorie`
  - `name` : Nom de la sous-catégorie (unique dans une catégorie donnée)
  - `description` : Description de la sous-catégorie
- **Relations** :
  - Appartient à une seule `Catégorie`.
  - Contient plusieurs `Listings`.

---

### Avis

- **Champs** :
  - `id` : Clé primaire
  - `user` : Auteur (clé étrangère vers `Utilisateur`)
  - `listing` : Listing évalué (clé étrangère vers `Listing`)
  - `rating` : Note (1 à 5)
  - `comment` : Texte du commentaire
  - `date_created` : Date de publication
- **Relations** :
  - Chaque avis est relié à un seul `Utilisateur` et à un seul `Listing`.

---

### Message

- **Champs** :
  - `id` : Clé primaire
  - `sender` : Expéditeur (clé étrangère vers `Utilisateur`)
  - `receiver` : Destinataire (clé étrangère vers `Utilisateur`)
  - `content` : Contenu du message
  - `date_sent` : Date d'envoi
- **Relations** :
  - Connecte deux `Utilisateurs`.

---

### Favoris

- **Champs** :
  - `id` : Clé primaire
  - `user` : Utilisateur (clé étrangère vers `Utilisateur`)
  - `listing` : Listing favorisé (clé étrangère vers `Listing`)
  - `date_added` : Date d'ajout
- **Relations** :
  - Relie un `Utilisateur` et un `Listing` (relation plusieurs-à-plusieurs).

---

## Optimisations Techniques

- **Indexation** :
  - Ajout d'index sur les champs : `username`, `email`, `category`, `subcategory`.
- **Caches** :
  - Utilisation de Redis pour la mise en cache des résultats de recherche et des favoris.
- **Optimisation ORM** :
  - Utilisation de `select_related` et `prefetch_related` pour réduire les requêtes redondantes.
- **Stockage des fichiers** :
  - Hébergement des images sur Cloudinary ou Amazon S3 pour minimiser la charge du serveur.
- **Scalabilité** :
  - Structure extensible pour ajouter des champs ou relations futurs.
- **Tests Unitaires** :
  - Validation des contraintes et relations via des tests avant migration.

---

**Diagramme Relationnel Simplifié** :

- **Utilisateur** (1) ↔ (1) **Profil**
- **Profil** (1) ↔ (N) **Listings**
- **Listing** (1) ↔ (1) **Catégorie**
- **Listing** (1) ↔ (1) **SousCatégorie**
- **Utilisateur** (1) ↔ (N) **Avis**
- **Utilisateur** (1) ↔ (N) **Messages** (envoyés et reçus)
- **Utilisateur** (M) ↔ (N) **Listings** (via Favoris)

## Sécurité et Modération

### EmailVerification

- **Champs** :
  - `id` : Clé primaire
  - `user` : Clé étrangère vers `Utilisateur`
  - `token` : Token unique de vérification
  - `created_at` : Date de création
  - `expires_at` : Date d'expiration
  - `verified_at` : Date de vérification
  - `is_verified` : Statut de vérification

### ReportReason

- **Champs** :
  - `id` : Clé primaire
  - `name` : Nom du motif
  - `description` : Description détaillée
  - `is_active` : Statut actif/inactif

### Report

- **Champs** :
  - `id` : Clé primaire
  - `reporter` : Utilisateur signalant (ForeignKey vers `Utilisateur`)
  - `content_type` : Type de contenu signalé (ContentType : Avis, Listing, Profil, etc.)
  - `content_id` : ID de l'objet signalé
  - `reason` : Clé étrangère vers `ReportReason`
  - `description` : Description détaillée du signalement
  - `status` : État du signalement (En attente, En cours, Résolu, Rejeté)
  - `created_at` : Date de création
  - `resolved_at` : Date de résolution
  - `resolved_by` : Modérateur ayant traité le signalement
  - `resolution_note` : Note de résolution

### ReviewModeration

- **Champs** :
  - `id` : Clé primaire
  - `review` : Clé étrangère vers `Avis`
  - `moderator` : Clé étrangère vers `Utilisateur` (modérateur)
  - `status` : État de la modération (En attente, Approuvé, Rejeté)
  - `moderation_date` : Date de modération
  - `moderation_note` : Note du modérateur
  - `automated_flags` : Drapeaux automatiques (contenu inapproprié, spam, etc.)

### Mise à jour de la table Avis

- **Nouveaux champs pour `Avis`** :
  - `moderation_status` : État de modération (En attente, Approuvé, Rejeté)
  - `is_visible` : Visibilité publique de l'avis
  - `last_modified` : Date de dernière modification

## Processus de Sécurité

1. **Vérification Email** :
   - Envoi automatique d'un email de vérification à l'inscription
   - Token avec expiration après 24h
   - Limitation des fonctionnalités jusqu'à vérification

2. **Modération des Avis** :
   - Vérification automatique du contenu (mots interdits, spam)
   - Mise en attente des avis signalés
   - Double validation pour les avis critiques (note ≤ 2/5)

3. **Gestion des Signalements** :
   - Notification immédiate aux modérateurs
   - Système de priorisation des signalements
   - Actions automatiques selon le nombre de signalements

## Diagramme Relationnel (ajouts)

- **Utilisateur** (1) ↔ (N) **Report** (signalements effectués)
- **Utilisateur** (1) ↔ (N) **ReviewModeration** (modérations effectuées)
- **Avis** (1) ↔ (1) **ReviewModeration**
- **Report** (N) ↔ (1) **ReportReason**

### Location

- **Champs** :
  - `coordinates` : Point géographique (latitude/longitude)
  - `address` : Adresse formatée
  - `city`, `region`, `country` : Données structurées

### Analytics

- Suivi des vues de profils
- Statistiques de recherche
- Métriques d'engagement

### Notification

- Notifications en temps réel
- Préférences de notification par utilisateur
- Historique des notifications

### Media

- Galerie photos pour les listings
- Gestion des documents (certificats, diplômes)
- Optimisation des images


## Analyse de la structure du modèle


### Points Forts du Modèle :
1.  Architecture Utilisateur :
   - Séparation claire Utilisateur/Profil
   - Système de rôles bien défini
   - Gestion multilingue avec Language
   - Intégration des réseaux sociaux via SocialMediaPlatform
2. Gestion des Listings :
   - Hiérarchie Catégorie → SousCatégorie → Listing
   - Système de tags flexible
   - Informations complètes (horaires, site web, localisation)
   - Statuts de validation
3. Sécurité et Modération :
   - Vérification email robuste
   - Système complet de modération des avis
   - Gestion des signalements
   - Traçabilité des actions
4. Relations et Interactions :
   - Système d'avis et notation
   - Gestion des favoris
   - Messagerie entre utilisateurs
   - Système de tags


### Points Forts Techniques :
1. Indexation appropriée des champs clés
2. Utilisation de Redis pour le cache
3. Stockage externe des médias
4. Structure extensible

### Recommandations pour l'Implémentation :
1. Mettre en place des tests unitaires solides
2. Implémenter une API REST documentée
3. Prévoir une stratégie de backup
4. Planifier la scalabilité



## Django Import-Export

```sh
# https://django-import-export.readthedocs.io/en/latest/installation.html 

pip install django-import-export


#1. Ajouter 'import_export' à INSTALLED_APPS
# settings.py
INSTALLED_APPS = (
    ...
    'import_export',
)

#2. Créer une ressource pour le modèle
# admin.py
#from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Listing


python manage.py collectstatic



from import_export.admin import ImportExportModelAdmin

class ListingResource(resources.ModelResource):
    class Meta:
        model = Listing