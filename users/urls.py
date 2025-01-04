from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'profiles', views.ProfileViewSet)
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'languages', views.LanguageViewSet)
router.register(r'social-platforms', views.SocialMediaPlatformViewSet)

app_name = 'users'

urlpatterns = [
    path('', include(router.urls)),
] 