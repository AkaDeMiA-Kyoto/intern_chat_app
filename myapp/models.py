from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    # 追加のフィールドを定義する
    image = models.ImageField(upload_to='media_local/', null=True, blank=True)


    # 既存のフィールドと関連名を変更する場合、related_nameを指定する
    groups = models.ManyToManyField(Group, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set')
    
    is_verified = models.BooleanField(default=False)

class Message(models.Model):
    message = models.CharField((""), max_length=50)
    send_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="send_message")
    receive_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="receive_message")
    date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['date']