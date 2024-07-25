from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
from ..models import Review, TrackScore
from ..serializers import ReviewSerializer, TrackScoreSerializer
from ..permissions import IsAdminOrAccountOwner

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrAccountOwner]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Review.objects.all()
        return Review.objects.filter(account__user=self.request.user)

    def perform_create(self, serializer):
        account = self.request.user.account
        serializer.save(account=account)
