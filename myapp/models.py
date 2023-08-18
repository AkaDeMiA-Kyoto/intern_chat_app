from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    image = models.ImageField(upload_to=None, height_field=None, width_field=None)

# TODO 不要
# モデルフォームでなくてもFormを作ることはできる。
# ModelsにはあくまでDatabaseに必要なものだけを書く。
class Content(models.Model):
    chat_content = models.CharField(max_length=2048)

class TalkContent(models.Model):
    #users = models.ForeignKey(TalkContent, on_delete=models.CASCADE)
    user_from = models.IntegerField()
    user_to = models.IntegerField()

    chat_content = models.CharField(max_length=2048)#ForeignKey(Content, on_delete=models.CASCADE)

    time = models.DateTimeField(auto_now_add=True)

    def get_content(self, **kwargs):
        friend_name = kwargs.get("username")

