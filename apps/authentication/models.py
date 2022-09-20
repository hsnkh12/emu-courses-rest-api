import resource
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..utils.models import UUIDModel
from ..courses.models import Resource


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


class Report(UUIDModel):

    REASON_CHOICES = (
        ('I','Invalid resource'),
        ('S','Spam or misleading'),
        ('M','Misinformation'),
        ('C','Captions issue')
    )

    resource = models.ForeignKey(
        Resource,
        on_delete= models.CASCADE,
        related_name= 'reports_related'
    )

    reason = models.CharField(
        max_length= 1,
        choices= REASON_CHOICES
    )

    checked = models.BooleanField(
        default= False
    )

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(
            user=instance
        )