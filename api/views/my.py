from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..serializers import AccountSerializer, ReviewSerializer
from ..models import Account, Review

class MyAccountView(viewsets.ReadOnlyModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

class MyReviewsView(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(account=self.request.user.account)
