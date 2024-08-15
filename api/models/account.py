from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='account', on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, default='')
    # ranking = models.IntegerField(null=True, blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
    def follow(self, account):
        Follow.objects.get_or_create(follower=self, following=account)

    def unfollow(self, account):
        Follow.objects.filter(follower=self, following=account).delete()

    def is_following(self, account):
        return Follow.objects.filter(follower=self, following=account).exists()

    def is_followed_by(self, account):
        return Follow.objects.filter(follower=account, following=self).exists()

class Follow(models.Model):
    follower = models.ForeignKey(Account, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(Account, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'], name='unique_follow')
        ]

    def clean(self):
        if self.follower == self.following:
            raise ValidationError('A user cannot follow themselves.')
        super().clean()
    
    def __str__(self):
        return f'{self.follower} is following {self.following}'
    