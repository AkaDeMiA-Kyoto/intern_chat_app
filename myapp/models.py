from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    icon = models.ImageField(
        verbose_name="画像", upload_to="uploads", default="image/noimage.png"
    )

class Talk(models.Model):
    talk = models.CharField(max_length=500)
    talk_from = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="talk_from"
    )
    talk_to = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="talk_to"
    )
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}>>{}".format(self.talk_from, self.talk_to)