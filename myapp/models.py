from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy
from django.utils import timezone


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='')
    REQUIRED_FIELDS = ['email', 'image']
    created_at = models.TimeField(auto_now_add=True)

# class Room(models.Model):
#     user1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user1')
#     user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user2')
#     created_at = models.TimeField(auto_now_add=True)

# class MessageManager(models.Manager):
#     def ordering(self, order='created_at'):
#         return self.get_queryset().order_by()

class Message(models.Model):
    # room = models.ForeignKey(Room, on_delete=models.CASCADE)
    send_from = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='send_from', default=1)
    send_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='send_to', default=1)
    content = models.TextField()
    send_at = models.DateTimeField(auto_now_add=True)