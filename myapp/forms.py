from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import Talk



class SignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', 'image')

class LoginForm(AuthenticationForm):
    class Meta:
        fields = ('username', 'password')
        
class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ('talk_content','talk_time','talk_to','talk_from')