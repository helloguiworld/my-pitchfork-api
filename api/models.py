from django.db import models

class Share(models.Model):
    TYPE_CHOICES = [
        ('square', 'Square'),
        ('stories', 'Stories'),
    ]
    
    album_id = models.CharField(max_length=50)
    album_name = models.CharField(max_length=100, default='Not specified')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    creation_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.album_id} - {self.type} ({self.creation_date})"