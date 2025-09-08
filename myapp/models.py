from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    image = models.ImageField("画像", upload_to='media_local', blank=True)