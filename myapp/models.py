from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    image = models.ImageField()
    date = models.DateTimeField(auto_now_add=True)
    view_date = models.CharField(max_length=5) # データベースに保存したくない
    message = models.CharField(max_length=500)

    def __str__(self):
        return self.username

class Message(models.Model):
    user_from = models.IntegerField()
    user_to = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=500) # max 500 length per one message