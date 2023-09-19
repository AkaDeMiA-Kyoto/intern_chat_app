from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CustomUser(AbstractUser):
    img = models.ImageField(default="default_profile_img.jpg", upload_to='../media_local/')
    date_joined = models.DateTimeField(auto_now_add=True)
# トーク内容を全てdatbaseに保存する形をとる
# ＞１個のトーク内容に紐づける情報は
# ＞〇誰が送ったのか
# ＞〇誰に送ったのか
# ＞〇いつ送ったのか
# という情報

# models.Modelを継承することにより、データベーステーブルとしてふるまうことを可能にしている
# related_name: 逆のリレーションシップを定義します。
# 関連先モデルから逆参照するための名前を指定します。
# 例えば、related_name="talk_from" とすることで、
# CustomUser モデルから Talk モデルにアクセスする際に talk_from 属性を使用できます。
# talk_fromとtalk_toはCusTomUserに逆参照できるように紐づけされている。
class Talk(models.Model):
    # メッセージ
    talk = models.CharField(max_length=500)
    # 誰から
    talk_from = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="talk_from")
    # 誰に
    talk_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="talk_to")
    # 時間は
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}>>{}".format(self.talk_from, self.talk_to)
    


# モデル＝テーブルの定義(データとデータベースのやり取りをする部分)
# 具体的には、テーブルにどんな値を保管するか、どんな項目があるか、
# といったことをモデルとして定義しておく
# レコード(中身) in テーブル(形式の定義) in データベース(入れ物)
# モデルのインスタンス = テーブルのレコード(Django超入門p143)
# モデルの書き方はFormクラスにそっくり
# フォームと同じようにクラスの中にはインスタンスを作成するが、django.db.modelsにあるクラス。
# テキストとの値を保管するフィールドはCharfieldだが、フィールドのforms.CharFieldクラスではなく、
# models.CharFirled。同じ名前でも、別のクラス。
# マイグレーションは、データベースの移行を行うための機能。
# あるデータベースから別のデータベースに移行するとき、
# 必要なテーブルを作成したりしてスムーズに移行できるようにするのがマイグレーション。
# マイグレーションではプロジェクトでデータベースをアップグレード、
# 例えば「データベースに何もない状態から、モデルをもとに必要なテーブルを作成する」という作業もできる。

