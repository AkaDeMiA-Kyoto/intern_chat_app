from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    image = models.FileField('Img')
    class Meta:
        verbose_name_plural = 'CustomUser'