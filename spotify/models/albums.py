from django.db import models

class Album(models.Model):
    id = models.CharField(primary_key=True, max_length=255, unique=True)
    name = models.CharField(max_length=255)
    data = models.JSONField()
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
