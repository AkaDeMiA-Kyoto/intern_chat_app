from .models import CustomUser, Talk_content
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.db import models
from django import forms

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from allauth.account.forms import SignupForm

class myUserForm(SignupForm):
    image = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = " "
        print()

    # class Meta:
    #     model = CustomUser
    #     fields = ("username", "email", "password1", "password2", "image")

class myLoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "Usename, または Password が違います",
        "inactive": "Username が登録されていません",
    }
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.label_suffix = " "

    class Meta:
        model = CustomUser

class ChatInputForm(forms.ModelForm):
    class Meta:
        model = Talk_content
        # exclude = ["user_from", "user_to"]
        fields = ("user_from","user_to","chat_content",)

class SearchFriendForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username",)

class ChangeInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = " "

class ChangeUserForm(ChangeInfoForm):
    class Meta:
        model = CustomUser
        fields = ("username",)


class ChangeEmailForm(ChangeInfoForm):
    class Meta:
        model = CustomUser
        fields = ("email",)

class ChangeIconForm(ChangeInfoForm):
    class Meta:
        model = CustomUser
        fields = ("image",)

class ChangePWForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = " "
    class Meta:
        model = CustomUser
        fields = ["password"]