from django.db import models

from django.contrib.auth.models import AbstractUser

from accounts.models import CustomUser

# Create your models here.


# class CustomUser(AbstractUser):
#     # username = models.CharField('name', max_length=40)
#     email = models.EmailField('メールアドレス')
#     image = models.ImageField('プロフィール画像', upload_to="uploads/")

#     def __str__(self):
#         return self.username


class Message(models.Model):
    message_from = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="from_name")
    message_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="to_name")
    message = models.CharField('トーク', max_length=128)
    sent_at = models.DateTimeField('送信日時', auto_now_add=True)

    def __str__(self):
        return self.message
