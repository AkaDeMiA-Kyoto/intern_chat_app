from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    image = models.FileField('Img')
    slug = models.SlugField(max_length=300, default="", null=False)
    class Meta:
        verbose_name_plural = 'CustomUser'

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender', null=True, blank=True)
    opposer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='opposer', null=True, blank=True)
    content = models.CharField(max_length=300)
    message_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '<Message:id=' + str(self.id) + ', ' + \
        '(' + str(self.message_date) + ')>'
    
    class Meta:
        verbose_name_plural = 'Message'
        ordering = ('message_date',)