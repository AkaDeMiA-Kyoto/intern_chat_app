from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import CustomUser
from django import forms

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required = True)

    class Meta:
        model = CustomUser
        fields = ("username", "email","profile_image", "password1", "password2")
        
class LoginForm(AuthenticationForm):
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)