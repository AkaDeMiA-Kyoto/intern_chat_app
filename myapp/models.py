from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.TextField(max_length=10, blank=False, null=False, unique=True)
    email = models.EmailField(unique=True)
    image = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    send_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="sent_messages",
    )

    send_to = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="received_messages",
    )

    content = models.TextField("content")

    created_at = models.DateTimeField(auto_now_add=True)
