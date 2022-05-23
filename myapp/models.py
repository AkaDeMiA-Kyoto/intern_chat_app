from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(("user name"),max_length=200, unique=True)
    email = models.EmailField(("email"),max_length=200)
    password1 = models.CharField(("password1"),max_length=200)
    password2 = models.CharField(("password2"),max_length=200)
    image = models.ImageField(("image"))
# Create your models here.
