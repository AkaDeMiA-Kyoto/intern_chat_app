from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.
class CustomUser(AbstractUser):
    img=models.ImageField(upload_to="img")

    def __str__(self):
        return self.username



class Talkroom(models.Model): 
    you = models.ForeignKey(CustomUser, related_name="you",on_delete=models.CASCADE)
    friend = models.ForeignKey(CustomUser, related_name="friend",on_delete=models.CASCADE,null=True)
    message = models.TextField()
    date = models.DateTimeField(default=timezone.now)

