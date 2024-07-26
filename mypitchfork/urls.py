from django.urls import path, include
from django.contrib import admin

# from rest_framework.routers import DefaultRouter
# from api.views import ShareClickViewSet
# router = DefaultRouter()
# router.register(r'-', -ViewSet)

urlpatterns = [
    path('', include('api.urls')),
    path('users/', include('users.urls')),
    path('spotify/', include('spotify.urls')),
    path('session-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
]
