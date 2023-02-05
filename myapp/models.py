from django.db import models
from django.contrib.auth.models import AbstractUser

# superuser name : marusu pass : gameisgood

# Create your models here.
class CustomUser(AbstractUser):
    icon_image = models.ImageField(upload_to='media_local')

class TalkRoomModel(models.Model): #ある二人の会話のトークルーム
    users = models.ManyToManyField(CustomUser) # idが小さいほうのユーザーをリストの0番目にする
    latest_message_date = models.DateTimeField(null=True)
    latest_message_content = models.TextField(null=True)
    
class MessageModel(models.Model):
    talk_room = models.ForeignKey(TalkRoomModel, on_delete=models.CASCADE)
    # speaker_name = models.CharField(max_length=10) 
    speaker_id = models.CharField(max_length=10) 
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    # 参考
    # Djangoでhidden属性でテンプレート出力する https://qiita.com/jansnap/items/17dd91cfd217b166a575

    # 【Django】Formに初期値を設定 4つの方法をまとめました https://itc.tokyo/django/form-with-initial-value/

    # DjangoのDateTimeFieldの詳しい使い方: 日付と時刻を扱うフィールド https://yu-nix.com/archives/django-datetimefield/

    # Djangoの多対多関係モデルで簡易タグ機能を作る https://qiita.com/aqmr-kino/items/5875c388d5fc405ee606
