from dataclasses import dataclass
from socket import send_fds
from weakref import WeakMethod
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import DateField
from django.utils import timezone

# Create your models here.
class CustomUser (AbstractUser):
    image = models.ImageField(verbose_name="プロフィール画像",upload_to = "media/" ,default='default/default_user.png')

class TalkContent (models.Model):
    date = models.DateTimeField("date_sent",default=timezone.now)
    send = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,related_name="send"
    )
    receive = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,related_name="receive"
    )
    sentence = models.CharField(max_length=200)
