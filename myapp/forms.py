from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm, Form
from .models import CustomUser, Message

class SignUpForm(UserCreationForm):
    
    username = forms.CharField(
        max_length=40,
    )
    
    email = forms.EmailField(
        required=True
    )
    
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        min_length=8
    )
    password2 = forms.CharField(
        label="Password(again)",
        widget=forms.PasswordInput(),
        min_length=8
    )
    image = forms.ImageField(
        label="Image",
        required=True
    )
    
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2", "image")

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs): # ???
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label

class MessageForm(ModelForm):
    message = forms.CharField(
        max_length=500,
        required=True,
        label=""
    )

    class Meta:
        model = Message
        fields = ("message",)

        error_messages = {
            "message": {
                "max_length": "Max 500 letters."
            }
        }