from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    username = models.CharField(("username"),max_length=200, unique=True)
    email = models.EmailField(("email"),max_length=200)
    password1 = models.CharField(("password1"),max_length=200)
    password2 = models.CharField(("password2"),max_length=200)
    image = models.ImageField( 'アイコン画像', upload_to='media/', default='default/light.png', blank=True)
    pub_data = models.DateTimeField("date signed up", default=timezone.now)

class Talk(models.Model):
    # メッセージ
    talk = models.CharField(max_length=500)
    # 誰から
    talk_from = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="talk_from")
    # 誰に
    talk_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="talk_to")
    # 時間は
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}>>{}".format(self.talk_from, self.talk_to)
# Create your models here.
