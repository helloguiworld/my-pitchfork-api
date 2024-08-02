from rest_framework import serializers
from django.db.models import Avg
from ..models import Album, Track
from api.models import Review

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

class AlbumCompleteSerializer(AlbumSerializer):
    data = serializers.SerializerMethodField()
    
    def get_data(self, obj):
        data = obj.data
        
        # TRACKS
        tracks = obj.tracks.all()
        data['tracks'] = [track.data for track in tracks]
        
        # REVIEWS
        reviews = obj.reviews.all()
        data['reviews_count'] = reviews.count()
        rs_avg = reviews.aggregate(Avg('score'))['score__avg']
        data['reviews_score_avg'] = round(rs_avg, 1) if rs_avg is not None else None
        
        return data
