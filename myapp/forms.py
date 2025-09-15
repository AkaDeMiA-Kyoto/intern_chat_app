from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Message
from django.contrib.auth.forms import AuthenticationForm 

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    icon = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'icon')

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'ユーザー名'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'パスワード'})

class ChatForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content', )
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'chatbox',
                'placeholder': 'メッセージを入力...',
                'autocomplete': 'off',
            })
        }

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username',)
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'ユーザー名を入力'
            })
        }

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'メールアドレスを入力'
            })
        }

class IconChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('icon',)
        widgets = {
            'icon': forms.FileInput(attrs={
                'placeholder': 'アイコンを選択'
            })
        }
