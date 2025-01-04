from django.http import JsonResponse
from utils.jwt_utils import JWTHandler
from django.conf import settings
from datetime import datetime, timezone, timedelta

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Exclure certains chemins de la vérification JWT
        if self._should_skip_jwt_auth(request.path):
            return self.get_response(request)

        # Vérifier le token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Token manquant'}, status=401)

        token = auth_header.split(' ')[1]
        payload, error = JWTHandler.validate_token(token)

        if error:
            return JsonResponse({'error': error}, status=401)

        # Ajouter les informations du token à la requête
        request.jwt_payload = payload
        request.user_id = payload.get('user_id')

        response = self.get_response(request)

        # Rafraîchir le token si nécessaire
        if self._should_refresh_token(payload):
            new_token, _ = JWTHandler.refresh_token(token)
            response['New-Token'] = new_token

        return response

    def _should_skip_jwt_auth(self, path):
        """Vérifie si le chemin doit être exclu de l'authentification JWT"""
        EXEMPT_PATHS = [
            '/api/auth/login/',
            '/api/auth/register/',
            '/admin/',
            '/static/',
            '/media/',
        ]
        return any(path.startswith(exempt_path) for exempt_path in EXEMPT_PATHS)

    def _should_refresh_token(self, payload):
        """Vérifie si le token doit être rafraîchi"""
        exp = datetime.fromtimestamp(payload['exp'])
        refresh_threshold = timezone.now() + timedelta(hours=1)
        return exp < refresh_threshold 