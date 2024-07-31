from rest_framework import serializers
from ..models import Album, Track

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

class AlbumWithTracksSerializer(AlbumSerializer):
    data = serializers.SerializerMethodField()
    
    def get_data(self, obj):
        data = obj.data
        tracks = obj.tracks.all()
        data['tracks'] = [track.data for track in tracks]
        return data
