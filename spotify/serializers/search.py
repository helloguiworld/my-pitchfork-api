from rest_framework import serializers
from ..models import Search
from .album import AlbumSerializer, AlbumWithTracksSerializer

class SearchSerializer(serializers.ModelSerializer):
    albums = serializers.SerializerMethodField()
    
    class Meta:
        model = Search
        fields = '__all__'
        
    def __init__(self, *args, album_serializer=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.album_serializer = album_serializer or AlbumWithTracksSerializer
    
    def get_albums(self, obj):
        albums = obj.albums.all().order_by('-updated_at')
        a_s = self.album_serializer(albums, many=True)
        albums = a_s.data
        return [album['data'] for album in albums]
        
class SearchSummarySerializer(SearchSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, album_serializer=AlbumSerializer, **kwargs)