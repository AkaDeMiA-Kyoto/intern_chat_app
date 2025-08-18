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

class NameForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=['username']
        widget=forms.TextInput(attrs={'class': 'large-text-input'})

class MailForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=['email']
        widget=forms.TextInput(attrs={'class': 'large-text-input'})

class ImageForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=['image']