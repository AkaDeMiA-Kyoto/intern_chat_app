from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField('お名前', max_length=200)
    email = models.EmailField('メールアドレス')
    password = models.CharField('パスワード', max_length=200)