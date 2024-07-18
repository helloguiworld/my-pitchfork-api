from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  SpotifyTokenView, SpotifySearchView, SpotifyAlbumView

# router = DefaultRouter()
# router.register(r'token', SpotifyTokenView, basename='spotify-token')
# router.register(r'search', SpotifySearchView, basename='spotify-search')

urlpatterns = [
    # path('', include(router.urls)),
    path('album/<str:id>/', SpotifyAlbumView.as_view(), name='spotify-album'),
    path('search/', SpotifySearchView.as_view(), name='spotify-search'),
    path('token/', SpotifyTokenView.as_view(), name='spotify-token'),
]
