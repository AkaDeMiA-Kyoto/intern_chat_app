from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='images/')

class Talk(models.Model):
    talk_content = models.CharField(max_length=200)
    talk_time = models.DateTimeField()
    talk_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="talk_to")
    talk_from = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="talk_from")

