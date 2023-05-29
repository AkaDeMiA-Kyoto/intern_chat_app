from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        max_length=40,
        required=True
    )
    email = forms.EmailField(
        label="Email",
        required=True
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        min_length=8
    )
    password2 = forms.CharField(
        label="Password(again)",
        widget=forms.PasswordInput(),
        min_length=8
    )
    image = forms.ImageField(
        label="Image",
    )
    
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2", "image")