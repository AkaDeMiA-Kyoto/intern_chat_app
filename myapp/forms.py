from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm 

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    icon = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'icon')

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'ユーザー名'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'パスワード'})