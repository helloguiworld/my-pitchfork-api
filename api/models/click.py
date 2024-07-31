from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class SearchClick(models.Model):
    q = models.CharField(max_length=50)
    
    creation_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.q} - {self.creation_date}"

class AlbumClick(models.Model):
    album_id = models.CharField(max_length=255)
    album_name = models.CharField(max_length=255)
    
    creation_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.album_name} - {self.creation_date}"

class ShareClick(models.Model):
    TYPE_CHOICES = [
        ('square', 'Square'),
        ('stories', 'Stories'),
    ]
    
    album_id = models.CharField(max_length=50)
    album_name = models.CharField(max_length=100, default='Not specified')
    review_score = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(Decimal('0.0')),
            MaxValueValidator(Decimal('10.0'))
        ],
        null=True,
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.album_id} - {self.type} ({self.creation_date})"