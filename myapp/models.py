from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import secrets


class User(AbstractUser):
    icon = models.ImageField(
        verbose_name="画像", upload_to="uploads"
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
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="talk_from"
    )
    # 誰に
    talk_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="talk_to")
    # 時間は
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}>>{}".format(self.talk_from, self.talk_to)
    
class EmailOTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="email_otps")
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    attempts = models.PositiveSmallIntegerField(default=0)

    @classmethod
    def create_for(cls, user, ttl_minutes=10):
        code = f"{secrets.randbelow(1_000_000):06d}"
        return cls.objects.create(
            user=user,
            code=code,
            expires_at=timezone.now() + timedelta(minutes=ttl_minutes),
        )

    def is_valid_now(self):
        return (not self.is_used) and (self.expires_at >= timezone.now()) and (self.attempts < 5)
