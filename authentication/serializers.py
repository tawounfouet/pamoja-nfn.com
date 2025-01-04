from rest_framework import serializers
from .models import (
    User,
    UserSession,
    TrustedDevice,
    SecurityEvent,
    SecurityPreference
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone_number', 'date_joined')
        read_only_fields = ('id', 'date_joined')

class UserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSession
        fields = ('id', 'device_type', 'ip_address', 'location', 'created_at', 'last_activity')
        read_only_fields = ('id', 'created_at')

class TrustedDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrustedDevice
        fields = ('id', 'device_name', 'device_type', 'is_trusted', 'trust_score', 'last_seen')
        read_only_fields = ('id', 'trust_score', 'last_seen')

class SecurityEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityEvent
        fields = ('id', 'event_type', 'description', 'severity', 'created_at', 'ip_address', 'location')
        read_only_fields = ('id', 'created_at')

class SecurityPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityPreference
        fields = ('require_2fa', 'notify_on_login', 'max_sessions', 'trusted_locations') 