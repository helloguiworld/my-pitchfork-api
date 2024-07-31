from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..serializers import AccountSerializer, ReviewSummarySerializer
from ..models import Account, Review
from ..permissions import HasAccount, IsAccountOwner

class MyAccountView(viewsets.ViewSet):
    permission_classes = [HasAccount]
    
    def list(self, request):
        user = request.user
        account = Account.objects.filter(user=user).first()
        serializer = AccountSerializer(account)
        return Response(serializer.data)

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
    permission_classes = [HasAccount]

    def list(self, request):
        account = request.user.account
        reviews = Review.objects.filter(account=account)
        serializer = ReviewSummarySerializer(reviews, many=True)
        
        # for review_data in serializer.data:
            
        
        return Response(serializer.data)


        