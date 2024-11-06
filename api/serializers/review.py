from rest_framework import serializers
from ..models import Review, TrackScore
from spotify.serializers import AlbumSerializer

class TrackScoreSerializer(serializers.ModelSerializer):
    score = serializers.DecimalField(
        max_digits=3,
        decimal_places=1,
        coerce_to_string=False
    )
    
    class Meta:
        model = TrackScore
        fields = '__all__'
        extra_kwargs = {
            'account': {'read_only': True},
            'review': {'read_only': True},
        }
        
class TrackScoreSummarySerializer(TrackScoreSerializer):
    class Meta:
        model = TrackScore
        fields = ['track', 'score']

class ReviewSerializer(serializers.ModelSerializer):
    track_scores = TrackScoreSerializer(many=True)
    score = serializers.DecimalField(
        max_digits=3,
        decimal_places=1,
        coerce_to_string=False
    )

    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {
            'account': {'read_only': True},
        }
        
    def create(self, validated_data):
        track_scores_data = validated_data.pop('track_scores', [])
        review = super().create(validated_data)
        self._create_or_update_track_scores(review, track_scores_data)
        return review
    
    def update(self, instance, validated_data):
        track_scores_data = validated_data.pop('track_scores', [])
        review = super().update(instance, validated_data)
        self._create_or_update_track_scores(review, track_scores_data)
        return review

    def _create_or_update_track_scores(self, review, track_scores_data):
        for track_score_data in track_scores_data:
            TrackScore.objects.update_or_create(
                account=review.account,
                track=track_score_data['track'],
                defaults={
                    'account': review.account,
                    'track': track_score_data['track'],
                    'review': review,
                    'score': track_score_data['score'],
                }
            )

class ReviewSummarySerializer(ReviewSerializer):
    track_scores = TrackScoreSummarySerializer(many=True)
    
    class Meta:
        model = Review
        fields = ['album', 'score', 'is_best_new', 'text', 'track_scores']

# ---------------------------------------------------------------------

class ReviewWithAlbumSerializer(ReviewSerializer):
    album = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['album', 'score', 'is_best_new', 'text']
    
    def get_album(self, obj):
        return obj.album.data

class ReviewWithAlbumAndTrackScoresSerializer(ReviewSummarySerializer, ReviewWithAlbumSerializer):
    pass