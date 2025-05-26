# API d'Authentification Pamoja

Cette API d'authentification complète fournit toutes les fonctionnalités nécessaires pour gérer l'authentification dans une application React avec Django.

## Fonctionnalités

- Authentification par JWT (JSON Web Token)
- Inscription et connexion classique (email/mot de passe)
- Authentification sociale (Google, GitHub)
- Gestion des profils utilisateurs
- Vérification d'email
- Réinitialisation de mot de passe

## Endpoints de l'API

### Endpoints JWT

Ces endpoints permettent de gérer l'authentification basée sur JWT.

- **POST /api/auth/jwt/create/** - Obtenir un nouveau token JWT
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
  
- **POST /api/auth/jwt/refresh/** - Rafraîchir un token
  ```json
  {
    "refresh": "your.refresh.token"
  }
  ```
  
- **POST /api/auth/jwt/verify/** - Vérifier un token
  ```json
  {
    "token": "your.access.token"
  }
  ```

### Endpoints Utilisateurs

- **GET /api/auth/me/** - Obtenir les détails de l'utilisateur connecté
- **GET /api/auth/social-accounts/** - Liste des comptes sociaux de l'utilisateur

### Endpoints d'Inscription et de Connexion

- **POST /api/auth/auth/registration/** - Inscription d'un utilisateur
  ```json
  {
    "email": "nouvel.utilisateur@example.com",
    "username": "nouvel_utilisateur",
    "password1": "motdepasse123",
    "password2": "motdepasse123"
  }
  ```

- **POST /api/auth/auth/login/** - Connexion
  ```json
  {
    "email": "utilisateur@example.com",
    "password": "motdepasse123"
  }
  ```

- **POST /api/auth/auth/logout/** - Déconnexion

### Endpoints de Gestion de Compte

- **POST /api/auth/users/reset_password/** - Demande de réinitialisation de mot de passe
- **POST /api/auth/users/reset_password_confirm/** - Confirmer la réinitialisation du mot de passe
- **POST /api/auth/users/activation/** - Activer un compte utilisateur

### Endpoints d'Authentification Sociale

- **GET /api/auth/auth/google/** - Connexion avec Google
- **GET /api/auth/auth/github/** - Connexion avec GitHub

## Exemples d'utilisation

### Connexion et obtention d'un token

```bash
# Connexion
curl -X POST http://localhost:8000/api/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### Utiliser le token pour accéder à une ressource protégée

```bash
# Accéder au profil utilisateur
curl -X GET http://localhost:8000/api/auth/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Intégration avec React

Pour l'intégration avec React, nous recommandons :

1. Utiliser un contexte d'authentification pour gérer l'état global
2. Configurer des intercepteurs Axios pour rafraîchir automatiquement les tokens
3. Stocker les tokens dans le localStorage ou dans des cookies HttpOnly

### Exemple de contexte d'authentification React

```jsx
// AuthContext.js
import React, { createContext, useState, useEffect, useContext } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Vérifier si l'utilisateur est connecté au chargement
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('accessToken');
      if (token) {
        try {
          // Configure axios with token
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
          
          // Get user info
          const res = await axios.get('/api/auth/me/');
          setUser(res.data);
        } catch (err) {
          // Token maybe expired, try refresh
          await refreshToken();
        } finally {
          setLoading(false);
        }
      } else {
        setLoading(false);
      }
    };
    
    checkAuth();
  }, []);

  // Fonction pour rafraîchir le token
  const refreshToken = async () => {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
      logout();
      return;
    }

    try {
      const res = await axios.post('/api/auth/jwt/refresh/', {
        refresh: refreshToken
      });
      
      localStorage.setItem('accessToken', res.data.access);
      axios.defaults.headers.common['Authorization'] = `Bearer ${res.data.access}`;
      
      // Get user info with new token
      const userRes = await axios.get('/api/auth/me/');
      setUser(userRes.data);
    } catch (err) {
      logout();
    }
  };

  // Fonction de connexion
  const login = async (email, password) => {
    try {
      setError(null);
      const res = await axios.post('/api/auth/jwt/create/', { email, password });
      
      localStorage.setItem('accessToken', res.data.access);
      localStorage.setItem('refreshToken', res.data.refresh);
      axios.defaults.headers.common['Authorization'] = `Bearer ${res.data.access}`;
      
      const userRes = await axios.get('/api/auth/me/');
      setUser(userRes.data);
      return true;
    } catch (err) {
      setError(err.response?.data || { detail: 'Erreur de connexion' });
      return false;
    }
  };

  // Fonction de déconnexion
  const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    delete axios.defaults.headers.common['Authorization'];
    setUser(null);
  };

  // Fonction d'inscription
  const register = async (userData) => {
    try {
      setError(null);
      await axios.post('/api/auth/auth/registration/', userData);
      return true;
    } catch (err) {
      setError(err.response?.data || { detail: 'Erreur d\'inscription' });
      return false;
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        error,
        login,
        logout,
        register,
        refreshToken
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
```

## Configuration et Déploiement

### Configuration des Fournisseurs Sociaux

1. Créer un projet dans la Google Developer Console
2. Créer une application sur GitHub
3. Configurer les clés API dans les paramètres Django
4. Configurer les URLs de redirection

### Exécuter le script de configuration

```bash
python authentication/create_social_apps.py
```

Ce script configurera automatiquement les applications sociales dans la base de données.

## Tests

Pour tester l'API d'authentification :

```bash
python authentication/test_auth_api.py
```

Ce script effectuera des requêtes de test sur tous les principaux endpoints.

## Sécurité

- Les tokens JWT ont une durée de vie limitée (15 minutes)
- Les tokens de rafraîchissement expirent après 7 jours
- Option pour cookies HttpOnly en production
- Protection CSRF activée
