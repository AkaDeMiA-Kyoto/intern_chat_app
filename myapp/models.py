from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField('メールアドレス' ,null=True)
    image = models.ImageField('アイコン',null=True)
    username = models.CharField(max_length=20,null=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []
    
class Talk(models.Model):
    talk_from = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='talk_from')
    talk_to = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='talk_to')
    talk_chat = models.CharField(max_length=100)
    talk_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.talk_chat