from django import forms
#from django.contrib.auth.forms import (
    #UserCreationForm,
    #AuthenticationForm,
    #PasswordChangeForm,
#)
from allauth.account.forms import (
    SignupForm,
    LoginForm,
    ChangePasswordForm,
)
from .models import User, Talk


class MySignupForm(SignupForm):
    img = forms.ImageField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'img')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'ユーザーネーム'
        self.fields['email'].label = 'メールアドレス'
        self.fields['password1'].label = 'パスワード'
        self.fields['password2'].label = 'パスワード確認'
        self.fields['img'].label = 'アイコン'

    def signup(self, request, user):
        user.img = self.cleaned_data['img']
        user.save()
        return user


class MyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].label = 'ユーザーネーム'
        self.fields['password'].label = 'パスワード'


class ChangeUsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', )
        labels = {
            'username': '新しいユーザーネーム',
        }


class ChangeEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', )
        labels = {
            'email': '新しいメールアドレス',
        }


class ChangeIconForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('img', )
        labels = {
            'img': '新しいアイコン',
        }


class MyChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['oldpassword'].label = '現在のパスワード'
        self.fields['password1'].label = '新しいパスワード'
        self.fields['password2'].label = '新しいパスワード確認'


class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ('message', )
        widgets = {
            'message': forms.Textarea,
        }