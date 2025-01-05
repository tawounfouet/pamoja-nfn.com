from django.urls import path
from .views import (
    ProfileListView, ProfileDetailView, ProfileCreateView,
    ProfileUpdateView, ProfileDeleteView
)

urlpatterns = [
    path('profiles/', ProfileListView.as_view(), name='profile-list'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/create/', ProfileCreateView.as_view(), name='profile-create'),
    path('profile/<int:pk>/update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/<int:pk>/delete/', ProfileDeleteView.as_view(), name='profile-delete'),
]