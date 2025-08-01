from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django import forms

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email address")
    image = forms.ImageField(label="image")
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email','image')

class LoginForm(AuthenticationForm):
    pass

