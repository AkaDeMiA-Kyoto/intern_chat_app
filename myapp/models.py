from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    groups=None
    user_permissions=None
    icon = models.ImageField()




class talk(models.Model):
    sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="sender")
    recipient = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="recipient")
    created_at=models.DateTimeField(auto_now_add=True)
    content=models.TextField()
    def __str__(self):
        return self.content
