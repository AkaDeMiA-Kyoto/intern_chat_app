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
    # 誰から
    message_from = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="message_from")
    # 誰へ
    message_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="message_to")
    # メッセージ内容
    talk = models.CharField('トーク', max_length=512)
    time = models.DateTimeField('送信日時', auto_now_add=True)

    class Meta:
        db_table = "message"

    def __str__(self):
        return "{}>{} {}".format(self.message_from, self.message_to, self.time)
