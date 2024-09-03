from django.db import models
# Django charField で min_length を設定するためのインポート
from django.core.validators import MinLengthValidator

from django.contrib.auth.models import AbstractUser

# Create your models here.


class Inquiry(models.Model):
    name = models.CharField('お名前', max_length=40)
    email = models.EmailField('メールアドレス')
    title = models .CharField('件名', max_length=128)
    contents = models.TextField('内容')
    posted_at = models.DateTimeField('お問い合わせ日時', auto_now_add=True)

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    # username = models.CharField('name', max_length=40)
    email = models.EmailField('メールアドレス')
    image = models.ImageField('プロフィール画像')

    def __str__(self):
        return self.username


class Message(models.Model):
    message_from = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="from_name")
    message_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="to_name")
    message = models.CharField('トーク', max_length=128)
    sent_at = models.DateTimeField('送信日時', auto_now_add=True)

    def __str__(self):
        return self.message
