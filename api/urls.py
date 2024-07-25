from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, ShareViewSet, SearchClickViewSet, AlbumClickViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'reviews', ReviewViewSet, basename='review')

router.register(r'share', ShareViewSet)
router.register(r'search-click', SearchClickViewSet)
router.register(r'album-click', AlbumClickViewSet)

urlpatterns = [
    path('', include(router.urls)),
]