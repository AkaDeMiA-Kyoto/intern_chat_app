from typing import Any
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.db import models
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField
from django.core.exceptions import ObjectDoesNotExist

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    image = forms.ImageField(required=True)
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'image')

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
    def clean_username(self):
        username = self.cleaned_data['username']
        return username
    def clean_password(self):
        password = self.cleaned_data['password']
        return password
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            user = get_user_model().objects.get(username=username)
        except ObjectDoesNotExist:
            raise forms.ValidationError("ユーザーが存在しません")
        if not user.check_password(password):
            raise forms.ValidationError("ユーザー名とパスワードが一致しません")
        # self.user_cache = user
    # def get_user(self):
    #     return self.user_cache