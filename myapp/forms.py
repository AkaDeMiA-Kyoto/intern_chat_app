from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth import forms as auth_forms
from .models import User, Talk

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'icon')
    
    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError(
            "パスワードが一致しませんでした。パスワードを入力し直してください。"
            )

class UsernameUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class EmailUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class IconUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['icon']

class PasswordUpdateForm(PasswordChangeForm):
    new_password1 = forms.CharField(
        label=("新しいパスワード"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=("新しいパスワード　（確認）"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )


class LoginForm(auth_forms.AuthenticationForm):
    '''ログインフォーム'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label 

class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ['content']
        labels = {
            'content': '',
        }
    
