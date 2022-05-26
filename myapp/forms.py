from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import User

User = get_user_model()


class SignUpForm(UserCreationForm):
    img = forms.ImageField(label="Img", required=False)
    class Meta:
        model = User
        fields = ('username','email')
