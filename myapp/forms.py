from django import forms
from django.db.models import fields 
from .models import Message, Talker

class TalkerForm(forms.ModelForm):
    class Meta:
        model = Talker
        fields = ['name', 'password', 'mail','image', ]


class SignupForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(min_length=8)
    conf_pass = forms.CharField(min_length=8)
    mail = forms.EmailField()
    image = forms.ImageField()

class LoginForm(forms.Form):
    name = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)

class NameAlterForm(forms.Form):
    newVal = forms.CharField(label="新しい名前")

class PassAlterForm(forms.Form):
    newVal = forms.CharField(label="新しいパスワード")

class MailAlterForm(forms.Form):
    newVal = forms.EmailField(label="新しいメールアドレス")

class ImageAlterForm(forms.Form):
    newVal = forms.ImageField(label="新しい画像")

class SendForm(forms.Form):
    content = forms.CharField(max_length=100)




        
    
