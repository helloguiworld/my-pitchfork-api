from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from ..models import Account

class Review(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    album = models.CharField(max_length=50)
    score = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(Decimal('0.0')),
            MaxValueValidator(Decimal('10.0'))
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def track_scores(self):
        return TrackScore.objects.filter(review=self)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['account', 'album'], name='unique_account_album')
        ]
        
    def __str__(self):
        return f"{self.account.user.username} - {self.album} - {self.score}"

class TrackScore(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    track = models.CharField(max_length=50)
    score = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(Decimal('0.0')),
            MaxValueValidator(Decimal('10.0'))
        ],
    )
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['account', 'track'], name='unique_account_track')
        ]

    def __str__(self):
        return f"{self.account.user.username} - {self.track} - {self.score}"
