from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth import password_validation
class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        label='Emailadress'
    )
    iamge = forms.ImageField(
        # upload_to='MEDIA_ROOT',
        label='img'
    )
    class Meta:
        model = CustomUser
        fields = ('username','email','password1','password2','iamge')