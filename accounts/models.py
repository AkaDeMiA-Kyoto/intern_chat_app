from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    # username = models.CharField('name', max_length=40)
    email = models.EmailField('メールアドレス')
    image = models.ImageField('プロフィール画像', upload_to="uploads/")

    class Meta:
        verbose_name_plural = 'CustomUser'

    def __str__(self):
        return self.username
