from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    img = models.ImageField(default="default_profile_img.jpg")
    

class Chat(models.Model):
    # 送った人、もらった人、いつ送ったか、送信内容
    send_from = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="送った人",
        related_name="chats_send",
    )
    send_to = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="もらった人",
        related_name="chats_received",
    )
    content = models.TextField(
        "送信内容",
        max_length=1000,
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(
        "送信時刻",
        auto_now_add=True,
    )
    
    pass