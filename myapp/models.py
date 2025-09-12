from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser): #デフォルトで存在するUserモデルには足りないものを追加
    Img = models.ImageField(upload_to='media_local', default='media_local/default.jpeg') #保存場所が引数として必要

    def __str__(self):
        return self.username

class Room(models.Model):
    participants = models.ManyToManyField(CustomUser, verbose_name='メンバー')

    def __str__(self):
        usernames = [user.username for user in self.participants.all()]
        # リスト内包表記
        # [<式> for <変数> in <イテラブル> if <条件>]
        return "Room: " + " & ".join(usernames)
        # 文字.join(イテラブル) は 文字列メソッド で、イテラブルの要素を結合して1つの文字列にする
        # " & " は区切り文字の部分
    
    @classmethod
    def get_or_create_room(cls, user_a, user_b):
        room = cls.objects.filter(participants=user_a).filter(participants=user_b).first()
        if room:
            return room
        room = cls.objects.create()
        room.participants.add(user_a, user_b)
        return room

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name="messages")
    sender = models.ForeignKey(CustomUser, verbose_name='送信者', on_delete=models.PROTECT)
    content = models.TextField(verbose_name='本文')
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)

    