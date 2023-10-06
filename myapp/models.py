from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    img =models.ImageField(default = 'default_img.png')

class Talk(models.Model):
    from_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='from_name')
    to_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='to_name')
    contents = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)
    

