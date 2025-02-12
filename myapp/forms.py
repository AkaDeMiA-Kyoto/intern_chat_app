from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    #UserCreationFormに含まれないフィールドの追加 requiredTrueで必須に
    email = forms.EmailField(required=True, label="Email")
    image = forms.ImageField(required=False, label="Image")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'image')
