from django.db import models

class Album(models.Model):
    id = models.CharField(primary_key=True, max_length=50, unique=True)
    data = models.JSONField()
    
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def name(self):
        return self.data.get('name', '')

    def __str__(self):
        return self.name

class Track(models.Model):
    id = models.CharField(primary_key=True, max_length=50, unique=True)
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    data = models.JSONField()
    
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def name(self):
        return self.data.get('name', '')

    def __str__(self):
        return self.name
