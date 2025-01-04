from django.urls import path
from .views import (
    LoginView,
    LogoutView,
    TokenRefreshView,
    TokenRevokeView,
    DeviceManagementView
)

app_name = 'authentication'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/revoke/', TokenRevokeView.as_view(), name='token_revoke'),
    path('devices/', DeviceManagementView.as_view(), name='device_list'),
    path('devices/<int:device_id>/', DeviceManagementView.as_view(), name='device_manage'),
] 