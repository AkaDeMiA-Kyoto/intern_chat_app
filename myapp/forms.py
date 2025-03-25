from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Signup, Message


class SingupForm(UserCreationForm):
    class Meta:
        model = Signup
        fields = ["username", "email", "password1", "password2", "img"]
    
    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise ValidationError("パスワードが一致しません。")
        
        if len(password1) < 8:
            raise ValidationError("パスワードは8文字以上です。")
        
        if username in password1 or password1 in username:
            raise ValidationError("ユーザーネームとパスワードが酷似しています。")

        return cleaned_data

class LoginForm(AuthenticationForm):
    pass

class MessageSend(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']