from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    age = models.IntegerField()
    country = models .CharField(max_length=50)
    gender = models.CharField(max_length=10)
    is_verified = models.BooleanField(default=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }