from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    img = models.ImageField(upload_to='img', default='asset/default-image.png')
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural='CustomUser'

class Message(models.Model): 
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="receiver", null=True)
    content = models.TextField()
    msg_date = models.DateTimeField(default=timezone.now)
