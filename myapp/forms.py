from cProfile import label
from tkinter import Widget
from unicodedata import name
from django import forms

class HelloForm(forms.Form):
    username = forms.CharField(label='username',\
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    emailaddress = forms.CharField(label='emailaddress',\
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'name@example.com'}))
    password = forms.CharField(label='password',\
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password (8-20 characters long)'}))
    passwordconfirmation = forms.CharField(label='passwordconfirmation',\
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password Confirm'}))
    img = forms.ImageField(label='img',\
        widget=forms.FileInput(attrs={'class':'form-control','id':'formFile'}))