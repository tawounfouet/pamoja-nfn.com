from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone

from .models import Profile, Notification, Language, SocialMediaPlatform
from .serializers import (
    ProfileSerializer,
    ProfileUpdateSerializer,
    NotificationSerializer,
    SocialLinkUpdateSerializer,
    ProfileSearchSerializer,
    LanguageSerializer,
    SocialMediaPlatformSerializer
)
from .services import ProfileService, NotificationService
from .permissions import IsProfileOwner, IsProfilePublic

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'bio']

    def get_queryset(self):
        if self.action == 'list':
            return Profile.objects.filter(is_public=True)
        return Profile.objects.all()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsProfileOwner]
        elif self.action in ['retrieve']:
            self.permission_classes = [IsAuthenticated, IsProfilePublic]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return ProfileUpdateSerializer
        elif self.action == 'search':
            return ProfileSearchSerializer
        return ProfileSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        filters = {
            'languages': request.query_params.getlist('languages', []),
            'location': request.query_params.get('location'),
            'verified': request.query_params.get('verified') == 'true'
        }
        
        profiles = ProfileService.search_profiles(
            query=query,
            filters=filters,
            user=request.user
        )
        
        page = self.paginate_queryset(profiles)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_social_links(self, request, pk=None):
        profile = self.get_object()
        serializer = SocialLinkUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            platform = serializer.validated_data['platform']
            username = serializer.validated_data['username']
            
            url = profile.add_social_link(platform, username)
            if url:
                return Response({'url': url})
            return Response(
                {'error': 'Plateforme invalide'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def view(self, request, pk=None):
        profile = self.get_object()
        ProfileService.record_profile_view(profile, request.user)
        return Response({'status': 'success'})

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        count = NotificationService.mark_notifications_as_read(request.user)
        return Response({'marked_read': count})

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = get_object_or_404(
            Notification,
            id=pk,
            user=request.user
        )
        notification.mark_as_read()
        return Response({'status': 'success'})

class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [IsAuthenticated]

class SocialMediaPlatformViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SocialMediaPlatform.objects.all()
    serializer_class = SocialMediaPlatformSerializer
    permission_classes = [IsAuthenticated]
