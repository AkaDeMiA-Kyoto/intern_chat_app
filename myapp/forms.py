from cProfile import label
from dataclasses import field
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    ##email=forms.EmailField(max_length=254,label='メールアドレス')
    ##prof_img=forms.FileField(label='プロフィール画像')

    class Meta:
        model=CustomUser
        fields = ['username','email','prof_img',]

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label