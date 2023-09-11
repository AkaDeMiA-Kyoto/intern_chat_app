
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User
from django.contrib.auth.forms import AuthenticationForm
"""
def SignUpForm()
"""
# User = get_user_model()

class SignupForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'icon')

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label