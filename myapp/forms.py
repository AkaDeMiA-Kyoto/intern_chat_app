from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


User = get_user_model()

class SignUpForm(UserCreationForm):
    # usable_password = None

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2","icon")

class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label

class UserIconForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['icon']
class UserNameForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username']
class UserMailForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email']