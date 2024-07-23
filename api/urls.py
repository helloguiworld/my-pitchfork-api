from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, ShareViewSet, SearchClickViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'share', ShareViewSet)
router.register(r'search-click', SearchClickViewSet)

urlpatterns = [
    path('', include(router.urls)),
]