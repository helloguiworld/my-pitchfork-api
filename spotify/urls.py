from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  SpotifyTokenView, SpotifySearchView, SpotifyAlbumView, ClientIpView
from .views import OldSearchesViewSet, OldAlbumsViewSet

router = DefaultRouter()
# router.register(r'token', SpotifyTokenView, basename='spotify-token')
# router.register(r'search', SpotifySearchView, basename='spotify-search')
router.register(r'old-searches', OldSearchesViewSet, basename='old-searches')
router.register(r'old-albums', OldAlbumsViewSet, basename='old-albums')

urlpatterns = [
    path('', include(router.urls)),
    path('ip', ClientIpView.as_view(), name='client-ip'),
    path('albums/<str:id>/', SpotifyAlbumView.as_view(), name='spotify-album'),
    path('search', SpotifySearchView.as_view(), name='spotify-search'),
    path('token', SpotifyTokenView.as_view(), name='spotify-token'),
]
