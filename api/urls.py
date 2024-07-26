from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, ShareClickViewSet, SearchClickViewSet, AlbumClickViewSet, ReviewViewSet
from .views.my import MyAccountView, MyReviewsView

router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='accounts')
router.register(r'reviews', ReviewViewSet, basename='reviews')

my_router = DefaultRouter()
my_router.register(r'account', MyAccountView, basename='my-account')
my_router.register(r'reviews', MyReviewsView, basename='my-reviews')

report_router = DefaultRouter()
report_router.register(r'search-click', SearchClickViewSet)
report_router.register(r'album-click', AlbumClickViewSet)
report_router.register(r'share-click', ShareClickViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('my/', include(my_router.urls)),
    path('report/', include(report_router.urls)),
]