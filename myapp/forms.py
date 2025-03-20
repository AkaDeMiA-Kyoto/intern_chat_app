from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Talk

class SignUpForm(UserCreationForm):
    #UserCreationFormに含まれないフィールドの追加 requiredTrueで必須
    email = forms.EmailField(required=True, label="Email")
    image = forms.ImageField(required=False, label="Image")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'image')

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser

# class TalkForm(forms.ModelForm):
#     class Meta:
#         model = Talk
#         fields = ['content']
