from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.
class CustomUser(AbstractUser):
    image=models.ImageField(upload_to="media_local")

class Talk(models.Model):
    sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name="sent_talks")
    recipient=models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name="received_talks")
    arrived_at=models.DateTimeField(default=timezone.now)
    message=models.CharField(max_length=500)
    class Meta:
        ordering=['arrived_at']