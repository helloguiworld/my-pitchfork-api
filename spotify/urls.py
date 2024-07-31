from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  SpotifyTokenView, SpotifySearchView, SpotifyAlbumView
from .views import OldSearchesViewSet, OldAlbumsViewSet

router = DefaultRouter()
router.register(r'token', SpotifyTokenView, basename='spotify-token')
router.register(r'search', SpotifySearchView, basename='spotify-search')
router.register(r'albums', SpotifyAlbumView, basename='spotify-album')
router.register(r'old-searches', OldSearchesViewSet, basename='old-searches')
router.register(r'old-albums', OldAlbumsViewSet, basename='old-albums')

urlpatterns = [
    path('', include(router.urls)),
]
