from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django import forms

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username","email", "image", "password1", "password2" )
        labels = {
            "username": ("ユーザー名:"),
            "email": ("メールアドレス:"),
            "image": ("画像:")
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # パスワードとパスワードの確認のラベルを変更
        self.fields['password1'].label = "パスワード:"
        self.fields['password2'].label = "パスワード（確認用）:"


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="ユーザーネーム:", max_length=30)
    password = forms.CharField(label="パスワード:",widget=forms.PasswordInput)