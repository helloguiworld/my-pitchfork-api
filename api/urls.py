from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, ShareViewSet, SearchClickViewSet, AlbumClickViewSet, ReviewViewSet
from .views.my import MyAccountView, MyReviewsView

my_router = DefaultRouter()
my_router.register(r'account', MyAccountView, basename='my-account')
my_router.register(r'reviews', MyReviewsView, basename='my-reviews')

MyReviewsView
router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='accounts')
router.register(r'reviews', ReviewViewSet, basename='reviews')

router.register(r'share', ShareViewSet)
router.register(r'search-click', SearchClickViewSet)
router.register(r'album-click', AlbumClickViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('my/', include(my_router.urls)),
]