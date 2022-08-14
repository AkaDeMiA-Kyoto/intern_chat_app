from tkinter import CASCADE
from urllib import request
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class CustomUser(AbstractUser):
    prof_img=models.ImageField(upload_to='',blank=True,null=True)

class CustomMessage(models.Model):
    primeUser=models.ForeignKey(CustomUser,on_delete=models.CASCADE,
    related_name="msg",null=False)
    subUser=models.ForeignKey(CustomUser,on_delete=models.CASCADE,
    related_name="dummyMsg",null=False)
    isReceipt=models.BooleanField(default=False)
    content=models.TextField()
    createdTime=models.DateTimeField()
    
