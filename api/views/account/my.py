from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
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
        
        user = request.user
        is_account_owner = user == account.user
        response['is_account_owner'] = is_account_owner
        
        a_s = AccountSerializer(account) if is_account_owner else AccountSummarySerializer(account)
        response['account'] = a_s.data
        
        reviews = Review.objects.filter(account=account).order_by('-score', '-created_at')
        
        response['reviews_count'] = reviews.count()
        
        top = reviews[:3]
        t_s = ReviewWithAlbumSerializer(top, many=True)
        top = t_s.data
        response['top'] = top
            
        return Response(response)


        