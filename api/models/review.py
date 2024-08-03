from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from ..models import Account
from spotify.models import Album, Track

class Review(models.Model):
    account = models.ForeignKey(Account, related_name='reviews', on_delete=models.CASCADE)
    album = models.ForeignKey(Album, related_name='reviews', on_delete=models.PROTECT)
    
    score = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(Decimal('0.0')),
            MaxValueValidator(Decimal('10.0'))
        ],
    )
    is_best_new = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return f"{self.account.user.username} - {self.album} - {self.score}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['account', 'album'], name='unique_account_album')
        ]

class TrackScore(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, related_name='scores', on_delete=models.PROTECT)
    review = models.ForeignKey(Review, related_name='track_scores', on_delete=models.CASCADE)
    
    score = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(Decimal('0.0')),
            MaxValueValidator(Decimal('10.0'))
        ],
    )
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['account', 'track'], name='unique_account_track')
        ]

    def __str__(self):
        return f"{self.account.user.username} - {self.track} - {self.score}"
