from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView

from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from .models import Talk
CustomUser = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username","email","password1","password2","image")




class LoginForm(AuthenticationForm):
    pass

class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ('talk_chat',)
        widgets = {"talk_chat": forms.TextInput(attrs={"autocomplete": "off"})}

class PasswordChangeForm(PasswordChangeForm):
    pass

class UserNameChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username',)
        labels = {"username":"新しいユーザー名"}

class MailChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email',)
        label = {"email":"新しいメールアドレス"}

class ImageChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('image',)
        label = {"image":"新しいアイコン"}

