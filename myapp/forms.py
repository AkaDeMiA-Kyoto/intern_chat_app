from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from .models import User, Talk


class SignupForm(forms.ModelForm):
    username = forms.CharField(label="ユーザー名")
    email = forms.EmailField(label="メールアドレス")
    icon = forms.ImageField(label="画像")
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ["username", "email", "icon", "password"]

    #パスワードのみバリデーションがいるのでsaveをオーバーライド
    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data["password"], user)
        user.set_password(self.cleaned_data["password"])
        user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="ユーザーネーム")
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput())

class TalkRoomForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
    message = forms.CharField(label="")
    class Meta:
        model = Talk
        fields = ["message"]

class UpdateUsernameForm(forms.ModelForm):
    username = forms.CharField(label="ユーザー名")
    class Meta:
        model = User
        fields = ["username"]

class UpdateMailaddressForm(forms.ModelForm):
    email = forms.EmailField(label="メールアドレス")
    class Meta:
        model = User
        fields = ["email"]

class UpdateIconForm(forms.ModelForm):
    icon = forms.ImageField(label="画像")
    class Meta:
        model = User
        fields = ["icon"]

