from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import models
from .models import CustomUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    image = forms.ImageField(required=True)
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'image')