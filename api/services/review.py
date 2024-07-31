from ..models import Review, TrackScore

def save_review(review_data, account):
    review = review_data
    track_scores = review.pop('track_scores')
    
    saved_review, _ = Review.objects.update_or_create(
        account=account,
        album=review['album'],
        defaults={
            'account': account,
            'album': review['album'],
            'score': review['score'],
            'is_best_new': review['is_best_new'],
        }
    )
    
    for track_score in track_scores:
        TrackScore.objects.update_or_create(
            account=account,
            track=track_score['track'],
            defaults={
                'account': account,
                'track': track_score['track'],
                'review': saved_review,
                'score': track_score['score'],
            }
        )
    
    return saved_review