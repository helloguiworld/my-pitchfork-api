from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import AuthenticatedUserView, PasswordResetRequestView

urlpatterns = [
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('auth-user/', AuthenticatedUserView.as_view(), name='authenticated-user'),
    path('token-auth/', obtain_auth_token, name='token_auth'),
]