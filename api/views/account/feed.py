from rest_framework import viewsets
from ...models import Review
from ...serializers import FeedSerializer
from ...paginations import ReviewPagination
from ...permissions import HasAccount

class FeedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FeedSerializer
    permission_classes = [HasAccount]
    
    pagination_class = ReviewPagination
    
    def get_queryset(self):
        account = self.request.user.account
        
        feed_accounts_ids = list(account.following.values_list('following__id', flat=True))
        feed_accounts_ids.append(account.id)
        
        return Review.objects.filter(account__id__in=feed_accounts_ids).order_by('-created_at')
    