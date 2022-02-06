from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Profile(AbstractUser):
    image=models.ImageField(upload_to='images/', default='', blank=True, null=True,)

    class Meta:
        verbose_name_plural = "Profile"