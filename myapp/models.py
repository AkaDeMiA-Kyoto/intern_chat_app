from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.


class MyUser(AbstractUser):
    # usernameとemailはすでにAbstractUserで定義済み,passwordはすでにAbstractBaseUserで定義済み
    img = models.ImageField(
        'アイコン画像', upload_to='media/%Y/%m/%d/', default='default/default_user.png')
    pub_date = models.DateTimeField("date signed up", default=timezone.now)


class ChatContent(models.Model):
    pub_date = models.DateTimeField("date sent")
    send_to = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='message_sent')
    send_from = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='message_was_sent')
    chat_content = models.CharField(max_length=1000)
