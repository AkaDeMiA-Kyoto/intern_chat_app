from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, default='None/default.png')

class Talk_content(models.Model):
    #users = models.ForeignKey(Talk_content, on_delete=models.CASCADE)
    user_from = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_from')
    user_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_to')

    chat_content = models.CharField(max_length=2048)#ForeignKey(Content, on_delete=models.CASCADE)

    time = models.DateTimeField(auto_now_add=True)

    def get_content(self, **kwargs):
        friend_name = kwargs.get("username")

