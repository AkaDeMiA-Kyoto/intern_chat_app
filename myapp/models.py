from django.db import models
from django.utils import timezone

class Talker(models.Model):
    name = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    mail = models.EmailField(max_length=100)
    image = models.ImageField(upload_to='files/',
        verbose_name='画像',)
    time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return  "[" + self.name +"]" + " (" +  str(self.mail) + ")"


class Message(models.Model):
    sender = models.ForeignKey(Talker, on_delete=models.CASCADE, related_name="sender")
    recipient = models.ForeignKey(Talker, on_delete=models.CASCADE, related_name="recipient")
    content = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
       # default=timezone.nowもok?

    def __str__(self):
        return self.content + ' (' + str(self.time) + ')'

    class Meta:
        ordering = ('time', )


 
