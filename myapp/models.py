from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.


class MyUser(AbstractUser):
    # usernameとemailはすでにAbstractUserで定義済み,passwordはすでにAbstractBaseUserで定義済み
    img = models.ImageField('アイコン画像', upload_to='media/%Y/%m/%d/', default='default/default_user_icon.png')
    pub_date = models.DateTimeField('登録日時', null=False, default=timezone.now)


class ChatContent(models.Model):

    class Meta:
        verbose_name='チャット内容'
        verbose_name_plural = 'チャット内容'
    
    pub_date = models.DateTimeField("date sent")
    send_to = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='message_sent')
    send_from = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='message_was_sent')
    chat_content = models.CharField(max_length=1000)

    def __str__(self):
        return self.chat_content
