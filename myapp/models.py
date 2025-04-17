from django.db import models
from django.contrib.auth.models import AbstractUser,User

class CustomUser(AbstractUser):
    image = models.ImageField('image')
    def __str__(self):
        return self.username

class ChatMessage(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='sender' ,related_name='sender')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='receiver',related_name='receiver')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.message    