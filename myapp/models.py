from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone
import uuid

# Create your models here.

class User(AbstractUser):
    image = models.ImageField(upload_to='image/', verbose_name="アイコン")
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username

class Message(models.Model):
    sender = models.UUIDField(default=uuid.uuid4, editable=False)
    receiver = models.UUIDField(default=uuid.uuid4, editable=False)
    contents = models.CharField(max_length=500)
    date_joined = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.contents