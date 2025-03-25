from django.db import models
from django.contrib.auth.models import AbstractUser

class Signup(AbstractUser):
    username = models.CharField(max_length=20, verbose_name="username", unique=True)
    email = models.EmailField(max_length=100, verbose_name="e-mailadress")
    password1 = models.CharField(max_length=100, verbose_name="password")
    password2 = models.CharField(max_length=100, verbose_name="password_comfirmation")
    img = models.ImageField(upload_to="images/", null=True, blank=True, verbose_name="icon",default="images/default.png")
    #last_chat_at = models.DateTimeField()
    class Meta:
        verbose_name_plural = "signup"

class Message(models.Model):
    message = models.CharField(max_length=200)
    sender = models.ForeignKey(Signup, on_delete=models.CASCADE, related_name="sender")
    recipient = models.ForeignKey(Signup, on_delete=models.CASCADE, related_name="recipient")
    user1 = models.IntegerField()
    user2 = models.IntegerField()
    sended_at = models.DateTimeField(auto_now_add=True) 
    last_sended_at = models.DateTimeField(auto_now=True)