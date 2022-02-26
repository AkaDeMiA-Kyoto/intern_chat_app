from cProfile import label
from tkinter import Widget
from unicodedata import name
from django import forms

class HelloForm(forms.Form):
    username = forms.CharField(label='username',\
        widget=forms.TextInput(attrs={'class':'form-control'}))
    emailaddress = forms.CharField(label='emailaddress',\
        widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='password',\
        widget=forms.TextInput(attrs={'class':'form-control'}))
    passwordconfirmation = forms.CharField(label='passwordconfirmation',\
        widget=forms.TextInput(attrs={'class':'form-control'}))
    img = forms.IntegerField(label='img',\
        widget=forms.NumberInput(attrs={'class':'form-control'}))