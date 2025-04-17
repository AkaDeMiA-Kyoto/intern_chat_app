from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import CustomUser
from django import forms
from .models import ChatMessage

class SignUpForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2','image')
class LogInForm(AuthenticationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'password')
class ChangeImageForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('image',)

class ChatMessageForm(forms.Form):
    message = forms.CharField(label='メッセージ' ,widget=forms.TextInput())