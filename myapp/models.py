from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name = ("メールアドレス"),
        unique = True
    )
    profile_image = models.ImageField(upload_to ='media_local', null = True, blank = True)
    def __str__(self):
        return self.username