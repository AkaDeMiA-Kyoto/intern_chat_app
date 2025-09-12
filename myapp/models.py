from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    image = models.ImageField("画像", blank=True)



User = get_user_model()

class Message(models.Model):
    # メッセージの送信者
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    # メッセージの受信者
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    # メッセージの内容
    content = models.TextField()
    # メッセージが作成された日時
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp'] # 最新のメッセージが上に来るように設定

    def __str__(self):
        return f'{self.sender.username} to {self.receiver.username}: {self.content[:20]}...'