from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import forms as authform

from myapp.models import MyUser

class SignUpForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('username', 'email', 'img')

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.fields['username'].label = 'ユーザー名'
        self.fields['username'].widget.attrs['placeholder'] = "新規ユーザー名..."
        self.fields['email'].label = 'メールアドレス'
        self.fields['email'].widget.attrs['placeholder'] = "aaa@example.com"
        self.fields['password1'].label = 'パスワード'
        self.fields['password1'].widget.attrs['placeholder'] = "新規パスワード..."
        self.fields['password2'].label = 'パスワード（確認）'
        self.fields['password2'].widget.attrs['placeholder'] = "再度入力してください..."

class LoginForm(authform.AuthenticationForm):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label

