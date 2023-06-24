from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    image = models.ImageField()

    def __str__(self):
        return self.username

class Message(models.Model):
    user_from = models.IntegerField()
    user_to = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=500) # max 500 length per one message