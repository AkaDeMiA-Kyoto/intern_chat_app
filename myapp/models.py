from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
from django.utils import timezone

# Create your models here.

class CustomUser(AbstractUser):
    img = models.ImageField(upload_to='media_local', null=True, blank=True)

class chat(models.Model):
    sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="sender")
    receiver = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="receiver")
    time = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=144)
