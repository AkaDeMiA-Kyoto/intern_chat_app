# from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import User
from django.core.exceptions import ValidationError

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'image']
        labels = { 'image' : 'アイコン' }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True

class LoginForm(AuthenticationForm):
    pass

class MessageForm(forms.Form):
    contents = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'placeholder':'Message form is here !'}))

class PasswordChangeForm(PasswordChangeForm):
    pass

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username'] 
        labels = { 'username' : '変更先ユーザー名' }

class ImageChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['image'] 
        labels = { 'image' : '変更先アイコン' }

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email'] 
        labels = { 'email' : '変更先メールアドレス' }





