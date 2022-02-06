from django.db import models
from django.db.models.fields import related
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    icon = models.ImageField(blank=True, null=True,default='グループ 481.png')
    userID = models.CharField(max_length = 15, null = True)
    username = models.CharField(
        verbose_name='ユーザーネーム',
        max_length=20,
        unique = True       
    )
    email = models.EmailField(
        max_length=254,
        null=True, 
        verbose_name='メールアドレス') 
 
class Talk(models.Model):
    f_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="from1")
    t_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="to1")
    content = models.CharField(max_length=300)
    pub_date = models.DateField(default=timezone.now)
    class Meta:
        ordering =  ('pub_date',)


  
