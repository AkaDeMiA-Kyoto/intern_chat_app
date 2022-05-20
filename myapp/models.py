from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class MyUser(AbstractUser):
      # usernameとemailはすでにAbstractUserで定義済み,passwordはすでにAbstractBaseUserで定義済み
    img = models.ImageField('アイコン画像',upload_to='media/%Y/%m/%d/')