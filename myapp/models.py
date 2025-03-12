from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils.timezone import now

class CustomUser(AbstractUser):
    username = models.CharField(verbose_name='Username', max_length=15, null=False, blank=False, unique=True)
    email = models.EmailField(verbose_name='Email', max_length=50, null=False, blank=False)
    password1 = models.CharField(verbose_name='Password', max_length=30, null=False, blank=False, default="")
    password2 = models.CharField(verbose_name='Password confirmation', max_length=30, null=False, blank=False, default="")
    image = models.ImageField(verbose_name='Img', upload_to="", blank=False, null=False, default="")
    
    def __str__(self):
        return self.username
    

class TalkLog(models.Model):
    fromuser = models.ForeignKey(CustomUser, related_name='fromuser', on_delete=models.CASCADE)
    touser = models.ForeignKey(CustomUser, related_name='touser', on_delete=models.CASCADE)
    message = models.TextField(verbose_name="message", null=False, blank=False)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.fromuser.username} > {self.touser.username} + {self.timestamp}"
    