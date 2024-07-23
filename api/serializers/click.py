from rest_framework import serializers
from ..models import SearchClick, AlbumClick

class SearchClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchClick
        fields = '__all__'
        
class AlbumClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumClick
        fields = '__all__'