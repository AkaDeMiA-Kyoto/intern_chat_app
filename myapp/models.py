from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class CustomUser(AbstractUser):
    email = models.EmailField(unique=False)
    image = models.ImageField(blank=True, null=True)


class Message(models.Model):
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="sent_messages",
    )

    send_to = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="received_messages",
    )

    content = models.TextField()

    created_at = models.DateTimeField(default=now)

