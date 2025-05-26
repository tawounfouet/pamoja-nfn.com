from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.routers import DefaultRouter
from .api_views import UserInfoView, SocialAccountViewSet

# Configuration du router pour les ViewSets
router = DefaultRouter()
router.register(r"social-accounts", SocialAccountViewSet, basename="social-account")

urlpatterns = [
    # JWT endpoints
    path("jwt/create/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # Djoser endpoints
    path("", include("djoser.urls")),
    # dj-rest-auth endpoints
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    # Social auth endpoints
    path("auth/google/", include("allauth.socialaccount.providers.google.urls")),
    path("auth/github/", include("allauth.socialaccount.providers.github.urls")),
    # Ajoutez d'autres fournisseurs selon vos besoins
    # Endpoints personnalisés
    path("me/", UserInfoView.as_view(), name="user-info"),
    path("", include(router.urls)),
]
