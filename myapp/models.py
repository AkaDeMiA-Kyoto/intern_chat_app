from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    nama = models.CharField(max_length = 200)
    email = models.CharField(max_length = 200)
    password = models.CharField(max_length = 200)


class Friend(models.Model):
    name = models.CharField(max_length = 200)

class Talk(models.Model):
    user_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    chat_partner_name = models.CharField(max_length = 200)
    message = models.CharField(max_length = 1000)
    date = models.DateTimeField()