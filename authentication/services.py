from django.utils import timezone
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db.models import Q
from user_agents import parse
from datetime import datetime, timedelta
import hashlib
import logging
from utils.ip_utils import IPInfoHandler
from utils.jwt_utils import JWTHandler

from .models import (
    User,
    UserSession,
    LoginAttempt,
    TrustedDevice,
    SecurityEvent,
    SecurityPreference,
    AuthToken,
    RevokedToken
)

# Configuration du logging
logger = logging.getLogger(__name__)

class DeviceManager:
    """Gestion des appareils et de leur niveau de confiance"""
    
    def __init__(self):
        self.ip_handler = IPInfoHandler()
        self.jwt_handler = JWTHandler()

    def get_client_ip(self, request):
        """Récupère l'IP du client en tenant compte des proxys"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def generate_device_id(self, request):
        """Génère un identifiant unique pour l'appareil"""
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        ip = self.get_client_ip(request)
        platform_data = str(parse(user_agent))
        
        device_string = f"{platform_data}|{ip}|{settings.DEVICE_ID_SALT}"
        return hashlib.sha256(device_string.encode()).hexdigest()

    def get_device_info(self, request):
        """Récupère les informations détaillées sur l'appareil"""
        user_agent_string = request.META.get('HTTP_USER_AGENT', '')
        user_agent = parse(user_agent_string)
        
        return {
            'browser': user_agent.browser.family,
            'browser_version': user_agent.browser.version_string,
            'os': user_agent.os.family,
            'os_version': user_agent.os.version_string,
            'device': user_agent.device.family,
            'is_mobile': user_agent.is_mobile,
            'is_tablet': user_agent.is_tablet,
            'is_pc': user_agent.is_pc
        }

    def analyze_device_risk(self, device, request):
        """Analyse le niveau de risque d'un appareil"""
        risk_score = 0
        risk_factors = []

        try:
            current_ip = self.get_client_ip(request)
            ip_details = self.ip_handler.get_ip_details(current_ip)
            
            if device.last_ip and ip_details:
                # Vérifier le changement de localisation
                if device.last_country != ip_details.get('country'):
                    risk_score += 25
                    risk_factors.append("Changement de pays détecté")

                # Vérifier la distance
                distance = self.ip_handler.calculate_distance(device.last_ip, current_ip)
                if distance and distance > 500:
                    risk_score += 20
                    risk_factors.append(f"Distance importante ({distance:.0f}km)")

            # Vérification du User-Agent
            current_ua = request.META.get('HTTP_USER_AGENT', '')
            if device.browser_info and current_ua != device.browser_info:
                risk_score += 15
                risk_factors.append("Changement de navigateur")

            # Vérification des tentatives de connexion
            recent_attempts = LoginAttempt.objects.filter(
                ip_address=current_ip,
                attempt_time__gte=timezone.now() - timedelta(hours=1)
            ).count()

            if recent_attempts > settings.MAX_LOGIN_ATTEMPTS_PER_HOUR:
                risk_score += 30
                risk_factors.append("Trop de tentatives de connexion")

        except Exception as e:
            logger.error(f"Erreur lors de l'analyse des risques: {str(e)}")
            risk_score += 10
            risk_factors.append("Erreur d'analyse")

        return risk_score, risk_factors

class SecurityService:
    """Service principal de sécurité"""

    def __init__(self):
        self.device_manager = DeviceManager()
        self.ip_handler = IPInfoHandler()
        self.jwt_handler = JWTHandler()

    def validate_login_request(self, request, user):
        """Valide une tentative de connexion"""
        try:
            device_id = self.device_manager.generate_device_id(request)
            ip_address = self.device_manager.get_client_ip(request)
            ip_details = self.ip_handler.get_ip_details(ip_address)

            # Vérifier le blocage temporaire
            block_key = f"login_block_{ip_address}"
            if cache.get(block_key):
                return False, "Trop de tentatives, veuillez réessayer plus tard"

            # Vérifier l'appareil
            device_info = self.device_manager.get_device_info(request)
            device, created = TrustedDevice.objects.get_or_create(
                user=user,
                device_id=device_id,
                defaults={
                    'device_name': f"{device_info['browser']} sur {device_info['os']}",
                    'device_type': 'mobile' if device_info['is_mobile'] else 'tablet' if device_info['is_tablet'] else 'desktop',
                    'browser_info': request.META.get('HTTP_USER_AGENT', ''),
                    'last_ip': ip_address,
                    'last_location': f"{ip_details.get('city', '')}, {ip_details.get('country', '')}",
                    'last_country': ip_details.get('country', '')
                }
            )

            # Analyser les risques
            risk_score, risk_factors = self.device_manager.analyze_device_risk(device, request)
            
            return True, {
                'device': device,
                'risk_score': risk_score,
                'risk_factors': risk_factors,
                'requires_2fa': risk_score >= 30 or created
            }

        except Exception as e:
            logger.error(f"Erreur de validation: {str(e)}")
            return False, "Erreur lors de la validation"

    def handle_successful_login(self, request, user):
        """Gère une connexion réussie"""
        device_id = self.device_manager.generate_device_id(request)
        device = TrustedDevice.objects.get(user=user, device_id=device_id)
        
        # Créer la session et les tokens
        tokens = self.jwt_handler.generate_token_pair(
            user_id=user.id,
            device_id=device_id
        )

        session = UserSession.objects.create(
            user=user,
            session_key=request.session.session_key,
            device_type=device.device_type,
            ip_address=self.device_manager.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            token=tokens['access']
        )

        return {
            'tokens': tokens,
            'session_id': session.id,
            'device_trusted': device.is_trusted
        }

    def end_user_sessions(self, user, exclude_session_id=None):
        """Termine toutes les sessions d'un utilisateur"""
        sessions = UserSession.objects.filter(user=user, is_active=True)
        if exclude_session_id:
            sessions = sessions.exclude(id=exclude_session_id)

        for session in sessions:
            if session.token:
                self.jwt_handler.revoke_token(session.token, "Session terminée")
            session.end_session() 