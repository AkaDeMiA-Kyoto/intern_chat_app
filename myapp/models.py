from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receive_messages')
    text = models.CharField(max_length=200)
    send_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.sender} to {self.receiver}: {self.text[:20]}'
    class Meta:
        ordering = ['-send_time']