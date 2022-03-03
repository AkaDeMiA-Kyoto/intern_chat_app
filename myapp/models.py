from email.policy import default
from django.db import models

class Friend(models.Model):
    username = models.CharField(max_length=100)
    emailadress = models.EmailField(max_length=200)
    password = models.CharField(max_length=100)
    passwordconfirmation = models.CharField(max_length=100)
    img = models.ImageField()

    def __str__(self):
        return '<Friend:id=' + str(self.id) + ',' + \
            self.username + '(' + str(self.emailadress) + ','+ str(self.password) + ')>'