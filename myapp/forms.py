from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import CustomUser, Friend

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'icon']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Friend
        fields = ['content']

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = self.instance.username

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and username != self.instance.username:
            if CustomUser.objects.filter(username=username).exists():
                raise forms.ValidationError("このユーザー名はすでに使用されています。")
        return username

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].initial = self.instance.email

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and email != self.instance.email:
            if CustomUser.objects.filter(email=email).exists():
                raise forms.ValidationError("このメールアドレスはすでに使用されています。")
        return email
    
class IconChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['icon']