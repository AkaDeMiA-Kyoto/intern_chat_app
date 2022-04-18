from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    icon = models.ImageField(
        verbose_name="画像", upload_to="uploads", default="images/noimage.png"
    )


# トーク内容を全てdatbaseに保存する形をとる
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
