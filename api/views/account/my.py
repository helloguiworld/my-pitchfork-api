from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from common.permissions import IsMyOriginOrAdmin
from ...serializers import (
    AccountSerializer,
    ReviewSummarySerializer,
    AccountSummarySerializer,
    ReviewWithAlbumSerializer
)
from ...models import Account, Review
from ...permissions import HasAccount, IsAccountOwner

class MyAccountView(viewsets.ViewSet):
    permission_classes = [HasAccount]
    
    def list(self, request):
        user = request.user
        account = Account.objects.get(user=user)
        a_s = AccountSerializer(account)
        return Response(a_s.data)

class MyReviewsView(viewsets.ModelViewSet):
    lookup_field = 'album'
    serializer_class = ReviewSummarySerializer
    permission_classes = [IsAccountOwner]

    def get_queryset(self):
        account = self.request.user.account
        return Review.objects.filter(account=account)

    def perform_create(self, serializer):
        account = self.request.user.account
        serializer.save(account=account)

class MyProfileView(viewsets.ViewSet):
    permission_classes = [IsMyOriginOrAdmin]

    @action(detail=False, methods=['get'], url_path='(?P<username>[^/]+)')
    def profile(self, request, username=None):
        try:
            account = Account.objects.get(user__username=username)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        response = {}
        
        # ACCOUNT OWNER FLAG
        user = request.user
        is_account_owner = user == account.user
        response['is_account_owner'] = is_account_owner
        
        # ACCOUNT
        a_s = AccountSerializer(account) if is_account_owner else AccountSummarySerializer(account)
        response['account'] = a_s.data
        
        # REVIEWS COUNT
        reviews = Review.objects.filter(account=account).order_by('-created_at')
        response['reviews_count'] = reviews.count()
        
        # NEW RELEASES (1 month = 4 weeks, max 8)
        max_new_releases = 12
        response['min_new_releases_to_unlock'] = 4
        one_month_ago = timezone.now() - timezone.timedelta(weeks=4)
        one_month_ago_str = one_month_ago.date().isoformat()
        new_releases = (
            reviews
                .filter(album__data__date__gte=one_month_ago_str)
                .order_by('-album__data__date', '-score', '-is_best_new')[:max_new_releases]
        )
        nr_s = ReviewWithAlbumSerializer(new_releases, many=True)
        new_releases = nr_s.data
        response['new_releases'] = new_releases
        
        # LATEST (max 20)
        max_latest = 20
        response['min_latest_to_unlock'] = 10
        latest = reviews[:max_latest]
        l_s = ReviewWithAlbumSerializer(latest, many=True)
        latest = l_s.data
        response['latest'] = latest
        
        return Response(response)


        