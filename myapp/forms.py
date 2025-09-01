from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from .models import CustomUser,chat
from django import forms
from django.db import models


class SignUpForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2','img')

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["username"] = "form-control"
            field.widget.attrs["password"] = "form-control"

class message(forms.ModelForm):

    class Meta:
        model = chat
        fields = ['content']

class MyPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# class changeusername(forms.ModelForm):

#     class Meta:
#         model = CustomUser
#         fields = ('username',)





