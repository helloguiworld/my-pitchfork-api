from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.db.models import Count, Avg, Sum
from common.permissions import IsMyOriginOrAdmin
from spotify.models import Album
from api.models import Account
from ..services.ranking import get_all_accounts_ranking

class AlbumRankingViewSet(viewsets.ViewSet):
    permission_classes = [IsMyOriginOrAdmin]
    
    def list(self, request):
        # NEW RELEASES (1 month = 4 weeks ago, ranking max 20)
        max_new_releases_ranking = 20
        one_month_ago = timezone.now() - timezone.timedelta(weeks=4)
        one_month_ago_str = one_month_ago.date().isoformat()
        new_releases_albums = (
            Album.objects
                .filter(data__date__gte=one_month_ago_str)
                .annotate(reviews_count=Count('reviews'))
                .filter(reviews_count__gt=0)
                .annotate(reviews_score_avg=Avg('reviews__score'), reviews_score_sum=Sum('reviews__score'))
                .order_by('-reviews_score_sum', '-reviews_count', '-data__date', 'data__name')[:max_new_releases_ranking]
        )
        new_releases_ranking = [{
            "position": position,
            "album": album.data,
            "reviews_count": album.reviews_count,
            "reviews_sum": album.reviews_score_sum,
            "reviews_avg": round(album.reviews_score_avg, 1),
        } for position, album in enumerate(new_releases_albums, start=1)]
        return Response(new_releases_ranking)

    @action(detail=False, methods=['get'])
    def year(self, request):
        # RELEASES OF THE YEAR (1 year ago, ranking max 20)
        max_year_releases_ranking = 20
        one_year_ago = timezone.now() - relativedelta(years=1)
        one_year_ago_str = one_year_ago.date().isoformat()
        year_releases_albums = (
            Album.objects
                .filter(data__date__gte=one_year_ago_str)
                .annotate(reviews_count=Count('reviews'))
                .filter(reviews_count__gt=0)
                .annotate(reviews_score_avg=Avg('reviews__score'), reviews_score_sum=Sum('reviews__score'))
                .order_by('-reviews_score_sum', '-reviews_count', '-data__date', 'data__name')[:max_year_releases_ranking]
        )
        year_releases_ranking = [{
            "position": position,
            "album": album.data,
            "reviews_count": album.reviews_count,
            "reviews_sum": album.reviews_score_sum,
            "reviews_avg": round(album.reviews_score_avg, 1),
        } for position, album in enumerate(year_releases_albums, start=1)]
        return Response(year_releases_ranking)
    
    @action(detail=False, methods=['get'])
    def all(self, request):
        # ALL ALBUMS (ranking max 20)
        max_all_ranking = 20
        all_albums = (
            Album.objects
                .annotate(reviews_count=Count('reviews')) 
                .filter(reviews_count__gt=0)
                .annotate(reviews_score_avg=Avg('reviews__score'), reviews_score_sum=Sum('reviews__score'))
                .order_by('-reviews_score_sum', '-reviews_count', '-data__date', 'data__name')[:max_all_ranking]
        )
        all_ranking = [{
            "position": position,
            "album": album.data,
            "reviews_count": album.reviews_count,
            "reviews_sum": album.reviews_score_sum,
            "reviews_avg": round(album.reviews_score_avg, 1),
        } for position, album in enumerate(all_albums, start=1)]
        return Response(all_ranking)
    
    
class AccountRankingViewSet(viewsets.ViewSet):
    permission_classes = [IsMyOriginOrAdmin]
    
    def list(self, request):
        # ALL ACCOUNTS (at least 1 review, ranking max 20)
        all_accounts_ranking = get_all_accounts_ranking(20)
        return Response(all_accounts_ranking)
