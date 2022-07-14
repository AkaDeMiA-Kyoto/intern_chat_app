from urllib import request
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class CustomUser(AbstractUser):
    prof_img=models.ImageField(upload_to='',blank=True,null=True)

class CustomMessage(models.Model):
    sender=models.IntegerField()
    receiver=models.IntegerField()
    content=models.TextField()
    createdTime=models.DateTimeField()
    
