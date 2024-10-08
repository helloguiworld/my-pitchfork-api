from rest_framework import serializers
from ..models import SearchClick, AlbumClick, ShareClick

class SearchClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchClick
        fields = '__all__'
        
class AlbumClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumClick
        fields = '__all__'
        
class ShareClickSerializer(serializers.ModelSerializer):
    review_score = serializers.DecimalField(
        max_digits=3,
        decimal_places=1,
        coerce_to_string=False
    )
    
    class Meta:
        model = ShareClick
        fields = '__all__'
