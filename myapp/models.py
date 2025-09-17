from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# Create your models here.
class CustomUser(AbstractUser):
    icon = models.ImageField(
        verbose_name="画像", upload_to="uploads", default="images/noimage.png"
    )

    def __str__(self):
        return f"({self.pk}) {self.username}"

class Friend(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recipient')
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

class Talk(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='me')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='you')
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=512)

    def __str__(self):
        return f"{self.sender.pk} > {self.recipient.pk}"
    
class Message(models.Model):
    message = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message}"