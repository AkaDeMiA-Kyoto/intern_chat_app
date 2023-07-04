from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    image = ProcessedImageField(
        default="default.jpeg",
        processors=[ResizeToFill(250, 250)],
        format='JPEG',
        options={'quality': 60}
    )

    def __str__(self):
        return self.username

class Message(models.Model):
    user_from = models.IntegerField()
    user_to = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=500) # max 500 length per one message