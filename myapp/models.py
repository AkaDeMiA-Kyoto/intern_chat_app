from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class CustomUser(AbstractUser):
    username = models.CharField(verbose_name='Username', max_length=15, null=False, blank=False, unique=True)
    email = models.EmailField(verbose_name='Email', max_length=50, null=False, blank=False)
    password1 = models.CharField(verbose_name='Password', max_length=30, null=False, blank=False, default="")
    password2 = models.CharField(verbose_name='Password confirmation', max_length=30, null=False, blank=False, default="")
    image = models.ImageField(verbose_name='Img', upload_to="", blank=False, null=False, default="")
    
    def __str__(self):
        return self.username