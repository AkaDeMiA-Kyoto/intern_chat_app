from django import forms
from .models import CustomUser

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.backends import AllowAllUsersModelBackend
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# class SignupModelForm(forms.ModelForm):
#     class Meta:
#         model = Signup

#         fields = ('username', 'email', 'password', 'password_conf', 'image')

class SignupForm(UserCreationForm):
    # Password-based authentication を削除するためのもの
    usable_password = None

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'image')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None


class LoginForm(AuthenticationForm):

    class Meta:
        model = CustomUser
        # fields = ('username', 'password')
