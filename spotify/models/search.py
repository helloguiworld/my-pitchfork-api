from django.db import models
from .albums import Album

class Search(models.Model):
    q = models.CharField(primary_key=True, max_length=50, unique=True)
    albums = models.ManyToManyField(Album, related_name='searches')
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.q
