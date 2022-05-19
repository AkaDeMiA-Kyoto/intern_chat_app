from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class MyUser(AbstractUser):
      # usernameとemailはすでにAbstractUserで定義済み
    password = models.CharField('パスワード', max_length=200)
    img = models.FileField('アイコン画像')