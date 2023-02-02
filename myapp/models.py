from django.db import models
from django.contrib.auth.models import AbstractUser

# superuser name : marusu pass : gameisgood

# Create your models here.
class CustomUser(AbstractUser):
    icon_image = models.ImageField(upload_to='media_local')

class TalkRoomModel(models.Model): #ある二人の会話のトークルーム
    users = models.ManyToManyField(CustomUser) # idが小さいほうのユーザーをリストの0番目にする
    
class MessageModel(models.Model):
    talkroom = models.ForeignKey(TalkRoomModel, on_delete=models.CASCADE)
    speaker = models.CharField(max_length=10) # user1のメッセージの場合はuser1,user2ならuser2
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    # 参考
    # https://yu-nix.com/archives/django-datetimefield/
    # https://qiita.com/aqmr-kino/items/5875c388d5fc405ee606
