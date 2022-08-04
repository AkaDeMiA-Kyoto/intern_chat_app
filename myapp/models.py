from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    img = models.ImageField(upload_to = "media/")

class Talk(models.Model):
    content = models.TextField()
    talk_from = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="talk_from")
    talk_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="talk_to")
    talk_at = models.DateTimeField(auto_now_add=True)
