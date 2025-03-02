from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Signup(AbstractUser):
    username = models.CharField(max_length=20, verbose_name="username", unique=True)
    email = models.EmailField(max_length=100, verbose_name="e-mailadress")
    password1 = models.CharField(max_length=100, verbose_name="password")
    password2 = models.CharField(max_length=100, verbose_name="password_comfirmation")
    image = models.ImageField(verbose_name="img")
