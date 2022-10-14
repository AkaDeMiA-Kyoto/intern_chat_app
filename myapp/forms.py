from allauth.account.forms import ChangePasswordForm
from .models import MyUser, ChatContent
from django import forms
from django.core.exceptions import ValidationError


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
    
    def clean_email(self):
        # emailに現在のemailと同じものを指定したときにバリデーションエラーを送出する
        if self.cleaned_data['email'] in MyUser.objects.values_list('email', flat=True):
            raise ValidationError('このメールアドレスはすでに使用されています。')
        return self.cleaned_data['email']


class MyPasswordChangeForm(ChangePasswordForm):
    """allauthのパスワード変更フォームのオーバーライド"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['oldpassword'].label = "現在のパスワード"
        self.fields['oldpassword'].widget.attrs['placeholder'] = "パスワードを入力..."
        self.fields['password1'].label = "新しいパスワード"
        self.fields['password1'].widget.attrs['placeholder'] = "新規パスワード..."
        self.fields['password2'].label = "新しいパスワード（確認）"
        self.fields['password2'].widget.attrs['placeholder'] = "再度入力してください..."

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
