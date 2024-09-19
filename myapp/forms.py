from django import forms
from .models import CustomUser, Message

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
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


class CustomPasswordChangeForm(PasswordChangeForm):

    class Meta:
        model = CustomUser


class MessageForm(forms.Form):
    message = forms.CharField(
        label='message',
        max_length=128,
        required=True
    )


class ChangeUsernameForm(forms.Form):
    username_new = forms.CharField(
        label='New Username',
        max_length=40,
        required=True,
    )


class ChangeEmailForm(forms.Form):
    email_new = forms.EmailField(
        label='New Address',
        required='True'
    )


class ChangeImageForm(forms.Form):
    image_new = forms.ImageField(
        label='New Icon',
        required=True
    )
