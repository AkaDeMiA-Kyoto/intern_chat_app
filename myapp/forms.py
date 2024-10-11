from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from .models import CustomUser, Message


class CustomUserCreationForm(UserCreationForm):
    profile_image = forms.ImageField(required=True)
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2',"profile_image")
    

class CustomAuthenticationForm(AuthenticationForm):
    code_form = forms.CharField(label=("認証コード"), max_length=30)
    

class UserSearchForm(forms.Form):
    query = forms.CharField(label='友達を検索', max_length=100)

class TalkForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("content",)
        widgets = {"content": forms.TextInput(attrs={"autocomplete": "off"})}

class UsernameUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username']  

class UseradressUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email']  

class UserimageUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_image']  

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password1', 'new_password2']