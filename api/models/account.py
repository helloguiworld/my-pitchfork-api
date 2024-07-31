from django.db import models
from django.conf import settings

class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, default='')
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
