from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    image = models.ImageField("画像")


class Message(models.Model):
    message = models.TextField("内容")
    time = models.DateTimeField("送信日時", default=timezone.now)
    sender = models.IntegerField("送信者")
    receiver = models.IntegerField("受信者")

    def __str__(self):
        return self.message

