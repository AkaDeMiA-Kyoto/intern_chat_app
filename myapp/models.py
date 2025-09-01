from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    image = models.ImageField(
        verbose_name="画像", 
        upload_to="user_image",
         blank=True, 
        )

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sent_massage")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="received_massage")
    content  = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True) 

    class Meta:
        indexes = [
            models.Index(fields=["sender","receiver","-created_at"])
        ]
        ordering = ["-created_at"]