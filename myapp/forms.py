from dataclasses import field
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import CustomUser,Chat

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','email','icon']

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username','password']

class FriendSearchForm(forms.Form):
    find = forms.CharField(label='Find',required=False)

class ChatSendForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['chat',]

class UpDateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','email','icon','password',]