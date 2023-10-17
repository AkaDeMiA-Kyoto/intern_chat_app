from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

from django.contrib.auth import get_user_model

from .models import Talk

User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "icon")

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")

class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ("talk",)
        widgets = {"talk": forms.TextInput(attrs={"autocomplete": "off"})}

class PasswordChangeForm(PasswordChangeForm):
    pass

class UsernameResetForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username",)

class MailResetForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)

class IconResetForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("icon",)

class FriendSearchForm(forms.Form):
    keyword = forms.CharField(
        label="検索",
    )