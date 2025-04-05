from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 

CustomUser = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 
                  'email', 
                  'password1', 
                  'password2', 
                  'user_icon'
                  )
        
class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        
class SettingForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'user_icon']