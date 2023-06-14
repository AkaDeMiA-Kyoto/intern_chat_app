from django.db import models
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
    iamge = models.ImageField(upload_to='MEDIA_ROOT')

# Create your models here.
