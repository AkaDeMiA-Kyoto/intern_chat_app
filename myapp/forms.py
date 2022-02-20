from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import TalkModel,User
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,UserChangeForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','password1','password2','icon']




class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.fields['username'].widget.attrs['class'] = 'form-control'
       self.fields['password'].widget.attrs['class'] = 'form-control'


class TalkForm(forms.ModelForm):
    class Meta:
        model = TalkModel
        fields = ['content']

class UsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class MailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class PasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
    



class UpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username','email','icon']

