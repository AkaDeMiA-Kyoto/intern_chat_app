from django.db import models
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
    iamge = models.ImageField(upload_to='MEDIA_ROOT')

class Talk(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='talks')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
# Create your models here.
