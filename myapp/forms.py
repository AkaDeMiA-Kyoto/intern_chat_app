
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm,
)
from .models import Talk, User

# User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email',"image")
        # fieldには必要なものだけを取り出す。

class LoginForm(AuthenticationForm):
    pass

class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ("talk",)
        widgets = {"talk": forms.TextInput(attrs={"autocomplete": "off"})}

class PasswordChangeForm(PasswordChangeForm):
    pass

class MailSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
        labels = {'email': '新しいユーザ名'}

class UserNameSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)
        labels = {'username': '新しいメールアドレス'}

class ImageSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('image',)
