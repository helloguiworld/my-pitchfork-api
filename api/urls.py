from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShareClickViewSet, SearchClickViewSet, AlbumClickViewSet
from .views.account import AccountViewSet, ReviewViewSet, FeedViewSet
from .views.account.my import MyAccountView, MyReviewsView, MyProfileView
from .views.ranking import AlbumRankingViewSet, AccountRankingViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='accounts')
router.register(r'reviews', ReviewViewSet, basename='reviews')

ranking_router = DefaultRouter()
ranking_router.register(r'album', AlbumRankingViewSet, basename='album')
ranking_router.register(r'account', AccountRankingViewSet, basename='account')

my_router = DefaultRouter()
my_router.register(r'account', MyAccountView, basename='my-account')
my_router.register(r'reviews', MyReviewsView, basename='my-reviews')
my_router.register(r'profile', MyProfileView, basename='my-profile')
my_router.register(r'feed', FeedViewSet, basename='my-feed')

report_router = DefaultRouter()
report_router.register(r'search-click', SearchClickViewSet)
report_router.register(r'album-click', AlbumClickViewSet)
report_router.register(r'share-click', ShareClickViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('ranking/', include(ranking_router.urls)),
    path('my/', include(my_router.urls)),
    path('report/', include(report_router.urls)),
]