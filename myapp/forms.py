from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm
class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        label='Emailadress'
    )
    iamge = forms.ImageField(
        # upload_to='MEDIA_ROOT',
        label='img'
    )
    class Meta:
        model = CustomUser
        fields = ('username','email','password1','password2','iamge')

class LoginForm(AuthenticationForm):
    # username = forms.
    class Meta:
        model = CustomUser
        fields = ('username','password')

class MessageForm(forms.Form):
    message = forms.CharField(widget=forms.TextInput(attrs={'class': 'message-input'}))

class IconUploadForm(forms.Form):
    new_icon = forms.ImageField()