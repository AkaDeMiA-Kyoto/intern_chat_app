from django import forms 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

from .models import CustomUser

class SignupForm(UserCreationForm):
    
    class Meta:
        model = CustomUser
        fields = ['username','email','img']
    
class CustomLoginForm(AuthenticationForm):
    pass
    
class CustomNameChangeForm(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = ["username"]
        
class CustomAddressChangeForm(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = ["email"]
        
class CustomIconChangeForm(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = ["img"]
        
       

