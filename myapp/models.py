from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    icon = models. ImageField(blank=True,upload_to='media')

class TalkModel(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    talkname = models.ForeignKey(User,on_delete=models.CASCADE,related_name='talkname')
    content = models.CharField(max_length=300)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('pub_date',)

