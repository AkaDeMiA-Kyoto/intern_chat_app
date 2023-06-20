from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
#from django.contrib.auth import forms as auth_forms
#これを書くと、止まるよ
# Create your models here.
class CustomUser(AbstractUser):
    # Email_address=models.EmailField(validators=[MinLengthValidator(6)],max_length=255)
    img =models.ImageField()

class Talk(models.Model):
    from_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='from_name')
    to_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='to_name')
    contents = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)
    
    
    
