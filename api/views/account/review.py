from rest_framework import viewsets
from ...models import Review
from ...serializers import ReviewSerializer
from ...paginations import ReviewPagination

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    pagination_class = ReviewPagination