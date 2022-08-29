from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    icon = models.ImageField(upload_to='media/images')
