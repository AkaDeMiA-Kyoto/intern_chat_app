from django import forms
from django.db.models import fields 
from .models import Message, Talker
from django.contrib.auth.forms import UserCreationForm


class TalkerForm(forms.ModelForm):
    class Meta:
        model = Talker
        fields = ['name', 'password', 'mail','image', ]


class SignupForm(UserCreationForm):
    username = forms.CharField(label="Username")
    password1 = forms.CharField(min_length=8, label="Password",widget=forms.PasswordInput )
    password2 = forms.CharField(min_length=8, label="Password confirmation", widget=forms.PasswordInput )
    mail = forms.EmailField(label="Email address")
    image = forms.ImageField(label="img")


class LoginForm(forms.Form):
    name = forms.CharField(max_length=100, label="ユーザーネーム")
    password = forms.CharField(max_length=100, label="パスワード")

class NameAlterForm(forms.Form):
    newVal = forms.CharField(label="新しい名前")

class PassAlterForm(forms.Form):
    newVal = forms.CharField(label="新しいパスワード")

class MailAlterForm(forms.Form):
    newVal = forms.EmailField(label="新しいメールアドレス")

class ImageAlterForm(forms.Form):
    newVal = forms.ImageField(label="新しい画像")

class SendForm(forms.Form):
    content = forms.CharField(max_length=100, label="")



        
    
