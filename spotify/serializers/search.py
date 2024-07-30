from rest_framework import serializers
from ..models import Search
from .album import AlbumSerializer

class SearchSerializer(serializers.ModelSerializer):
    albums = serializers.SerializerMethodField()
    
    class Meta:
        model = Search
        fields = '__all__'
    
    def get_albums(self, obj):
        albums = obj.albums.all().order_by('updated_at')
        album_serializer = AlbumSerializer(albums, many=True)
        return [album['data'] for album in album_serializer.data]
    
class SearchSummarySerializer(serializers.ModelSerializer):
    albums = serializers.SerializerMethodField()
    
    class Meta:
        model = Search
        fields = '__all__'
    
    def get_albums(self, obj):
        albums = obj.albums.all().order_by('updated_at')
        album_serializer = AlbumSerializer(albums, many=True)
        
        albums = []
        for album_obj in album_serializer.data:
            album_data = album_obj['data']
            
            album_data['total_tracks'] = len(album_data['tracks'])
            del album_data['tracks']
            
            albums.append(album_data)
            
        return albums