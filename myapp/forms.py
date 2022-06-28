import email
from email.message import EmailMessage
from email.mime import image
from sre_constants import SUCCESS
from django.contrib.auth.forms import UserCreationForm 
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import CustomUser, TalkContent
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.core.mail import EmailMessage

class SignUpForm(UserCreationForm):
  
    class Meta:
        model = CustomUser
        # fields = ("username","password1","password2","email","image")
        fields = ("username","password1","password2","email","image")



class LoginForm (AuthenticationForm):
    def __init__(self, *args,**kwargs) :
        super().__init__( *args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

class TalkForm(forms.ModelForm):
    class Meta:
        model = TalkContent
        fields = ("sentence",)

class UsernameChangeForm(forms.ModelForm):
    
    class Meta:
        model  = CustomUser
        fields = ("username",)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
    def clean_username(self):
        Username = self.cleaned_data['username']
        CustomUser.objects.filter(username=Username, is_active=False).delete()
        return Username

class EmailChangeForm(UsernameChangeForm):
    class Meta:
        model  = CustomUser
        fields = ("email",)

    def clean_username(self):
        Email = self.cleaned_data['email']
        CustomUser.objects.filter(email=Email, is_active=False).delete()
        return Email

class IconChangeForm(UsernameChangeForm):
    class Meta:
        model  = CustomUser
        fields = ("image",)

    def clean_username(self):
        Image = self.cleaned_data['image']
        CustomUser.objects.filter(image=Image, is_active=False).delete()
        return Image

class InquiryForm (forms.Form):
    name = forms.CharField(label='お名前',max_length=30)
    email = forms.EmailField(label='メアド')
    title = forms.CharField(label='タイトル',max_length=30)
    message = forms.CharField(label='本文',widget=forms.Textarea)

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        title = self.cleaned_data['title']
        message = self.cleaned_data['message']

        subject = 'お問い合わせ{}'.format(title)
        message = '送信者名:{0}\nメアド:{1}\nメッセージ:\n{2}'.format(name,email,message)
        from_email = 'admin@example.com'
        to_list = [
            'test@example.com'
        ]
        cc_list = [
            email
        ]

        message = EmailMessage(subject = subject,body = message,from_email=from_email,to=to_list,cc=cc_list)
        message.send()