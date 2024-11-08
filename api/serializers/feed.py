from rest_framework import serializers
from ..models import Review
from .review import ReviewWithAlbumSerializer
from .account import AccountUserSummarySerializer

class FeedSerializer(serializers.ModelSerializer):
    review = ReviewWithAlbumSerializer(source='*')
    account_user = AccountUserSummarySerializer(source='account.user')
    
    class Meta:
        model = Review
        fields = ['review', 'account_user', 'created_at']