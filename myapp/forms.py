from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Message
from django import forms

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password1",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        min_length=8,
        error_messages={
            "min_length": "Passwords must contain at least 8 words.",
        },
    )
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'image']

class SendMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username']

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email']

class IconChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['image']