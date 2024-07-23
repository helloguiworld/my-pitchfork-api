from django.db import models

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
        return f"{self.q} - {self.creation_date}"