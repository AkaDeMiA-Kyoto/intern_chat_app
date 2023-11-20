from collections.abc import Mapping
from typing import Any
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm
from django import forms
from django.db import models
from django.forms.utils import ErrorList
from .models import CustomUser, ImageChange
from django.contrib.auth import get_user_model
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
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        try:
            user = get_user_model().objects.get(username=username)
        except ObjectDoesNotExist:
            raise forms.ValidationError("ユーザーが存在しません")
        if not user.check_password(password):
            raise forms.ValidationError("ユーザー名とパスワードが一致しません")
    
        # self.user_cache = user
    # def get_user(self):
    #     return self.user_cache

class MessageForm(forms.Form):
    content = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'メッセージを入力'}))

class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        # self.fields['new_password1'].widget.attrs['placeholder'] = '半角英数字８文字以上'# placeholderの指定
        # self.fields['new_password2'].widget.attrs['placeholder'] = 'パスワード確認用'

class EmailChangeForm(forms.Form):
    old_email = forms.EmailField(required=True)
    new_email1 = forms.EmailField(required=True)
    new_email2 = forms.EmailField(required=True)
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.current_user = user
    def clean(self):
        old_email = self.cleaned_data['old_email']
        new_email1 = self.cleaned_data['new_email1']
        new_email2 = self.cleaned_data['new_email2']
        if old_email != self.current_user.email:
            raise forms.ValidationError('元のパスワードが違います')
        if new_email1 != new_email2:
            raise forms.ValidationError('２つのパスワードが一致しません')

class UsernameChangeForm(forms.Form):
    old_username = forms.CharField(required=True)
    new_username1 = forms.CharField(required=True)
    new_username2 = forms.CharField(required=True)
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.current_user = user
    def clean(self):
        old_username = self.cleaned_data['old_username']
        new_username1 = self.cleaned_data['new_username1']
        new_username2 = self.cleaned_data['new_username2']
        if old_username != self.current_user.username:
            raise forms.ValidationError('元のユーザー名が違います')
        if new_username1 != new_username2:
            raise forms.ValidationError('２つのユーザー名が違います')

class ImageChangeForm(forms.ModelForm):
    class Meta:
        model = ImageChange
        fields = ['image']