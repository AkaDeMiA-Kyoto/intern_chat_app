from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class CustomUser(AbstractUser, UserManager):

    email = models.EmailField(verbose_name='メールアドレス', unique=True, blank=False, null=False)
    thumbnail = models.ImageField(upload_to='images/thumbnail/', verbose_name='サムネイル', blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email