from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='media_local')
    created_at = models.DateTimeField(auto_now_add=True, null=True) #ユーザーの登録日時
    

#友人情報を格納するFriendsテーブルクラスの定義
# class Friends(models.Model):
#     class Meta:
#         verbose_name = '友達リスト' #verbose_nameはモデルやモデルフィールド、アプリの名前を指定するもの。管理画面でのモデルの名前を日本語で指定。
#         verbose_name_plural = '友達リスト' #pluralは複数形指定らしい

#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name = "user_friends") #related_nameは逆参照 on_deleteは削除の際の挙動を指示
#     friends = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="友達", related_name = "friend_friends") #ForeignKeyは1対多

#     def __str__(self):
#         return f"{self.friend}"

#自分が関連してるトークの絞り込み
class Talk(models.Model):
    send_user =models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="send_user",null=True)
    recieve_user =models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="recieve_user",null=True)
    talk_at = models.DateTimeField(auto_now_add=True,null=True)
    content = models.CharField(max_length=3000) 