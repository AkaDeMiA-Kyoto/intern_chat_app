from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,AuthenticationForm,PasswordChangeForm
from .models import CustomUser,Talk

class CustomUserForm(UserCreationForm):
    
    class Meta:
        model = CustomUser
        fields = ('username','email','password1','password2','img')
        
class loginform(AuthenticationForm):
    
    class Meta:
        model = CustomUser
        #オーバーライドできない
        
class TalkForm(forms.ModelForm):
     class Meta:
        model = Talk
        fields = ('contents',)
        # widgets={'from_name':forms.HiddenInput(),
        #          'to_name':forms.HiddenInput(),
        #          'time':forms.HiddenInput(),}

