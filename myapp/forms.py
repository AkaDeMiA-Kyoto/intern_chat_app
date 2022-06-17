from email.mime import image
from sre_constants import SUCCESS
from django.contrib.auth.forms import UserCreationForm 
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import CustomUser, TalkContent
from django.contrib.auth.forms import AuthenticationForm
from django import forms

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