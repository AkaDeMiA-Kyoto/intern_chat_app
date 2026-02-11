from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='media_local', null=True, blank=True)
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

class TalkRoom(models.Model):
    user_low = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dm_low")
    user_high = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dm_high")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user_low", "user_high"], name="unique_dm_pair")
        ]

class Message(models.Model):
    room = models.ForeignKey(TalkRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)