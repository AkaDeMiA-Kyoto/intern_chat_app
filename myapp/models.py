from email.policy import default
from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    icon = models.ImageField(upload_to='images')

    def __str__(self):
        return '<id = ' + str(self.id) + ' name = ' + self.username + '>'

class Chat(models.Model):
    chat_to = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='chat_to')
    chat_from = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='chat_from')
    chat = models.CharField(max_length=300)
    pub_date = models.DateTimeField(auto_now_add=True)