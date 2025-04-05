from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    user_icon = models.ImageField('プロフィール画像',upload_to='user_icons',default="img/head_icon.png")
    
    def __str__(self):
        return f"{self.username},{self.id}"
    
class Talk(models.Model):
    message = models.CharField('メッセージ',max_length=500)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages',verbose_name='送信者')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages',verbose_name='受信者')
    created_at = models.DateTimeField('送信日時',auto_now_add=True)
    
    class Meta:
       ordering = ["-created_at"]
       
    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}: {self.message[:30]}"