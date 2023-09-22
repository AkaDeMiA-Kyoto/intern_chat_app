from django.db import models
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
    iamge = models.ImageField(upload_to='MEDIA_ROOT')

class Talk(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_talks', on_delete=models.CASCADE,null=True)
    receiver = models.ForeignKey(CustomUser, related_name='received_talks', on_delete=models.CASCADE, null=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} - {self.receiver.username} - {self.message}'
# Create your models here.
