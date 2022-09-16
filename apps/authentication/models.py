from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..utils.models import UUIDModel
# Create your models here.


class User(AbstractUser,UUIDModel):

    email = models.EmailField(
        max_length=60,
        unique=True,
        help_text= 'Gmail or Privateemail'
    )

    first_name = None
    last_name = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(
            user=instance
        )