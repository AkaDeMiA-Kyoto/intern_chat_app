from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name = ("メールアドレス"),
        unique = True
    )
    profile_image = models.ImageField(upload_to ='media_local', null = True, blank = True)
    def __str__(self):
        return self.username
    
class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name="send_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name="receive_messages", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        ordering = ['-timestamp']