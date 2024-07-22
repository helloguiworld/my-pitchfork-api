from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, ShareViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'share', ShareViewSet)

urlpatterns = [
    path('', include(router.urls)),
]