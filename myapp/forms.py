from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth.views import AuthenticationForm
from .models import Talk
from django import forms
from django.contrib.auth import update_session_auth_hash

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2", "icon")

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "password")

class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ['content']

class UserChangeForm(forms.ModelForm):
    username = forms.CharField(max_length=30, required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs.get('instance', None)
        self.fields['username'].widget.attrs['class'] = 'form-control'
    class Meta:
        model = User
        fields = (
            "username",
        )

class EmailChangeForm(forms.ModelForm):
    email = forms.EmailField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs.get('instance', None)
        self.fields['email'].widget.attrs['class'] = 'form-control'
    class Meta:
        model = User
        fields = (
            "email",
        )

class IconChangeForm(forms.ModelForm):
    icon = forms.ImageField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs.get('instance', None)
        self.fields['icon'].widget.attrs['class'] = 'form-control'
    class Meta:
        model = User
        fields = (
            "icon",
        )