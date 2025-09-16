from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    icon = models.ImageField(null=True,default="/default.png")
    def __str__(self):
            return self.username
    
class Talk(models.Model):
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    talk_from = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="talks_sent")
    talk_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="talks_received")
    content = models.CharField(max_length=300, default='')
    def __str__(self):
            return self.content
    
