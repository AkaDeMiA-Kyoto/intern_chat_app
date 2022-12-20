from django.db import models
from django.contrib.auth.models import AbstractUser

# superuser name : marusu pass : gameisgood

# Create your models here.
class CustomUser(AbstractUser):
    icon_image = models.ImageField(upload_to='media_local')
