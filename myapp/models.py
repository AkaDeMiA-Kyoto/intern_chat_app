from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    image = models.ImageField(
        upload_to="uploads",null=True
    )
    def __str__(self):
        return self.username
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

class Talk(models.Model):
    talk = models.CharField(max_length=500)
    talk_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="talk_sent")
    talk_from = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="talk_receive")
    talk_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.talk

# Create your models here.
