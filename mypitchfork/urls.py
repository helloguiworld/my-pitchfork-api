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
from api.views import ShareViewSet

router = DefaultRouter()
router.register(r'share', ShareViewSet)

urlpatterns = [
    # path('auth-user/', AuthenticatedUserView.as_view(), name='authenticated-user'),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
