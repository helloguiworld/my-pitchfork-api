from rest_framework import serializers
from ..models import Review, TrackScore

class TrackScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackScore
        fields = '__all__'
        extra_kwargs = {
            'account': {'read_only': True},
            'review': {'read_only': True},
        }

class ReviewSerializer(serializers.ModelSerializer):
    track_scores = TrackScoreSerializer(many=True)

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
                    'score': track_score_data['score'],
                    'review': review
                }
            )