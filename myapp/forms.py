from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm,
)
from .models import User

# User = get_user_model()


class SignUpForm(UserCreationForm):
    # img = forms.ImageField(label="Img", required=True)
    class Meta:
        model = User
        fields = ('username','email',"image")
        # fieldには必要なものだけを取り出す。

class LoginForm(AuthenticationForm):
    pass
