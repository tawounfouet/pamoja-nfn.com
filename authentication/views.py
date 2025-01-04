from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .services import SecurityService, DeviceManager
from .models import (
    User,
    UserSession,
    SecurityEvent,
    TrustedDevice,
    LoginAttempt
)
from utils.jwt_utils import JWTHandler

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response(
                {'error': 'Email et mot de passe requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'Identifiants invalides'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        security_service = SecurityService()
        
        # Valider la tentative de connexion
        is_valid, validation_result = security_service.validate_login_request(request, user)
        if not is_valid:
            return Response(
                {'error': validation_result},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Authentifier l'utilisateur
        user = authenticate(request, email=email, password=password)
        if not user:
            LoginAttempt.objects.create(
                email=email,
                ip_address=DeviceManager().get_client_ip(request),
                status=LoginAttempt.Status.FAILED
            )
            return Response(
                {'error': 'Identifiants invalides'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Vérifier si 2FA est requis
        if validation_result.get('requires_2fa'):
            request.session['pending_user_id'] = user.id
            return Response({
                'requires_2fa': True,
                'message': 'Vérification en deux étapes requise'
            })

        # Connexion réussie
        login(request, user)
        login_result = security_service.handle_successful_login(request, user)

        return Response({
            'message': 'Connexion réussie',
            'tokens': login_result['tokens'],
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.get_full_name()
            }
        })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        security_service = SecurityService()
        security_service.end_user_sessions(
            request.user,
            exclude_session_id=request.session.get('current_session_id')
        )
        logout(request)
        return Response({'message': 'Déconnexion réussie'})

class TokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'error': 'Refresh token requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        tokens, error = JWTHandler.refresh_token_pair(refresh_token)
        if error:
            return Response(
                {'error': error},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        return Response(tokens)

class TokenRevokeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response(
                {'error': 'Token requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        success, error = JWTHandler.revoke_token(
            token,
            reason=request.data.get('reason')
        )
        
        if not success:
            return Response(
                {'error': error},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        return Response({'message': 'Token révoqué avec succès'})

class DeviceManagementView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Liste tous les appareils de l'utilisateur"""
        devices = TrustedDevice.objects.filter(user=request.user)
        return Response([{
            'id': device.id,
            'name': device.device_name,
            'type': device.device_type,
            'last_used': device.last_seen,
            'is_trusted': device.is_trusted,
            'is_current': device.device_id == DeviceManager().generate_device_id(request)
        } for device in devices])

    def post(self, request):
        """Marque un appareil comme approuvé"""
        device_id = request.data.get('device_id')
        if not device_id:
            return Response(
                {'error': 'ID de l\'appareil requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            device = TrustedDevice.objects.get(
                user=request.user,
                id=device_id
            )
            device.is_trusted = True
            device.trust_score = 100
            device.save()

            SecurityEvent.log_event(
                user=request.user,
                event_type=SecurityEvent.EventType.DEVICE_TRUSTED,
                description=f"Appareil approuvé: {device.device_name}",
                severity=1
            )

            return Response({'message': 'Appareil approuvé avec succès'})
        except TrustedDevice.DoesNotExist:
            return Response(
                {'error': 'Appareil non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, device_id):
        """Révoque la confiance d'un appareil"""
        try:
            device = TrustedDevice.objects.get(
                user=request.user,
                id=device_id
            )
            
            # Terminer toutes les sessions associées
            UserSession.objects.filter(
                user=request.user,
                device_type=device.device_type,
                is_active=True
            ).update(
                is_active=False,
                expires_at=timezone.now()
            )

            device.is_trusted = False
            device.trust_score = 0
            device.save()

            SecurityEvent.log_event(
                user=request.user,
                event_type=SecurityEvent.EventType.DEVICE_UNTRUSTED,
                description=f"Appareil révoqué: {device.device_name}",
                severity=2
            )

            return Response({'message': 'Appareil révoqué avec succès'})
        except TrustedDevice.DoesNotExist:
            return Response(
                {'error': 'Appareil non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
