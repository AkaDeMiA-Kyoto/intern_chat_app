from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
)

from .models import CustomUser


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required = True)

    class Meta:
        model = CustomUser
        fields = ("username", "email","profile_image", "password1", "password2")
        
class LoginForm(AuthenticationForm):
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username'
        ]

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'email'
        ]
class IconChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'profile_image'
        ]