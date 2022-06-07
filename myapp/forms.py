from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import MyUser, ChatContent
from django import forms


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


class LoginForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label


class ChatForm(forms.ModelForm):

    class Meta:
        model = ChatContent
        fields = ('chat_content',)
        widgets = {
            # cssクラスの追加
            'chat_content': forms.TextInput(attrs={'class': 'content-input', 'placeholder': 'ここにテキストを入力...'})
        }


class NameChangeForm(forms.ModelForm):

    class Meta:
        model = MyUser
        fields = ('username',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'username-input', 'placeholder': '新しいユーザー名'})
        }
        labels = {
            'username': '新しいユーザー名'
        }


class EmailChangeForm(forms.ModelForm):

    class Meta:
        model = MyUser
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'email-input', 'placeholder': 'aaa@example.com'})
        }
        labels = {
            'email': '新しいメールアドレス'
        }


class MyPasswordChangeForm(PasswordChangeForm):
    """パスワード変更フォームのオーバーライド"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = "現在のパスワード"
        self.fields['old_password'].widget.attrs['placeholder'] = "パスワードを入力..."
        self.fields['new_password1'].label = "新しいパスワード"
        self.fields['new_password1'].widget.attrs['placeholder'] = "新規パスワード..."
        self.fields['new_password2'].label = "新しいパスワード（確認）"
        self.fields['new_password2'].widget.attrs['placeholder'] = "再度入力してください..."

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class IconChangeForm(forms.ModelForm):

    class Meta:
        model = MyUser
        fields = ('img',)
        widgets = {
            'img': forms.FileInput(attrs={'class': 'img-input'})
        }
        labels = {
            'img': '新しいアイコン'
        }
