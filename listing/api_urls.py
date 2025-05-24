from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    CategoryViewSet,
    SubCategoryViewSet,
    ListingViewSet,
    ReviewViewSet,
    MediaViewSet,
)

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"subcategories", SubCategoryViewSet)
router.register(r"listings", ListingViewSet)
router.register(r"reviews", ReviewViewSet)
router.register(r"media", MediaViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
