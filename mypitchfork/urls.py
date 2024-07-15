"""
URL configuration for mypitchfork project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

# from users.views import AuthenticatedUserView
# from rest_framework.authtoken.views import obtain_auth_token
from api.views import ShareViewSet

router = DefaultRouter()
router.register(r'share', ShareViewSet)

urlpatterns = [
    # path('auth-user/', AuthenticatedUserView.as_view(), name='authenticated-user'),
    # path('api/token-auth/', obtain_auth_token, name='api_token_auth'),
    path('session-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
