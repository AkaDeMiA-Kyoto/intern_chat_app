from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser,Talk
from django import forms

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email address")
    image = forms.ImageField(label="image")
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email','image')


class LoginForm(AuthenticationForm):
    pass

class MessageForm(forms.Form):
    message=forms.CharField(max_length=500,label=None,widget=forms.TextInput(attrs={'class': 'large-text-input'}))
    class Meta:
        model=Talk
        fields=['message']

class NameForm(forms.Form):
    a= forms.CharField(label="New username",widget=forms.TextInput(attrs={'class': 'large-text-input'}))

class MailForm(forms.Form):
    a= forms.EmailField(label="New Email address",widget=forms.TextInput(attrs={'class': 'large-text-input'}))

class ImageForm(forms.Form):
    a= forms.ImageField(label="New icon")