from django.contrib.auth.forms import  AuthenticationForm, PasswordChangeForm, UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "image")

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        
