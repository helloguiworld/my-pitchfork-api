from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, name, password=None):
        """
        Creates and saves a user with the given username, email, name, and password.
        """
        if not username:
            raise ValueError('Users must have an username')
        if not email:
            raise ValueError('Users must have an email')
        if not name:
            raise ValueError('Users must have a name')
        
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            name=name
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, name, password=None):
        """
        Creates and saves a superuser with the given username, email, first_name,
        surname and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            name=name,
            password=password
        )
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=50)
    
    date_joined = models.DateTimeField(default=timezone.now, editable=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'name']

    class Meta:
        verbose_name = "user"

    def __str__(self):
        return self.username
