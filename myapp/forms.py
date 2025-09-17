from django import forms
from .models import CustomUser, Talk
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2','icon']

class LoginForm(AuthenticationForm):
    pass

class TalkModelForm(forms.ModelForm): 
    class Meta:
        model = Talk
        fields = ['content']

class UsernameChangeForm(forms.Form): 
    username = forms.CharField(max_length=100, label='新しいユーザー名')

class EmailChangeForm(forms.Form): 
    email = forms.EmailField(max_length=100, label='新しいメールアドレス')

class IconChangeForm(forms.Form): 
    icon = forms.FileField(label='画像')
