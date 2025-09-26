from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

<<<<<<< HEAD
from datetime import datetime, timedelta
from django.utils import timezone
import random

class User(AbstractUser):
    icon = models.ImageField(
        verbose_name="画像", upload_to="uploads", default="images/noimage.png"
    )


# トーク内容を全てdatabaseに保存する形をとる
# ＞１個のトーク内容に紐づける情報は
# ＞〇誰が送ったのか
# ＞〇誰に送ったのか
# ＞〇いつ送ったのか
# という情報
class Talk(models.Model):
    # メッセージ
    talk = models.CharField(max_length=500)
    # 誰から
    talk_from = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="talk_from"
    )
    # 誰に
    talk_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="talk_to")
    # 時間は
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}>>{}".format(self.talk_from, self.talk_to)
    


def generate_passcode():
    return random.randint(100000, 999999)

class OTPCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    passcode = models.CharField(max_length=6, default=generate_passcode)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timedelta(minutes=5) >= timezone.now() - self.created_at
=======
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
>>>>>>> 568a137c735e2253106d8e0a27f94eeb14bead04
