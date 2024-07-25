from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import AuthenticatedUserView, PasswordResetRequestView, PasswordResetView

urlpatterns = [
    path('password-reset-request', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset/<u_id_b64>/<token>/', PasswordResetView.as_view(), name='password_reset_request'),
    path('auth-user', AuthenticatedUserView.as_view(), name='authenticated_user'),
    path('token-auth', obtain_auth_token, name='token_auth'),
]