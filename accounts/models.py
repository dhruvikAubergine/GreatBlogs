from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail


#
class User(AbstractUser):
    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    country = models .CharField(max_length=50)
    is_verified = models.BooleanField(default=False)

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


@receiver(post_save, sender=User)
def send_update_profile_email(sender, instance, **kwargs):
    user = sender.objects.get(id=instance.id)
    subject = 'GreatBlog Account Information'
    message = f'Hi {user.username},\nYour profile details is updated.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    send_mail(subject, message, email_from, recipient_list)

