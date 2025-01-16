from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    image = models.ImageField('image')
    def __str__(self):
        return self.username