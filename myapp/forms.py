from email.policy import default
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm,
)
from .models import Talk, User
from allauth.account.forms import (
    LoginForm,
    SignupForm,
    ResetPasswordForm,
    ResetPasswordKeyForm,
)

# User = get_user_model()

# allauth実装前
# class SignUpForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('username','email',"image")
        # fieldには必要なものだけを取り出す。

# allauth実装前
# class LoginForm(AuthenticationForm):
#     pass

class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ("talk",)
        widgets = {"talk": forms.TextInput(attrs={"autocomplete": "off"})}

class PasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['placeholder'] = '元のパスワード'
        self.fields['new_password1'].widget.attrs['placeholder'] = '新しいパスワード'
        self.fields['new_password2'].widget.attrs['placeholder'] = '新しいパスワード(確認用)'
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class MailSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
        labels = {'email': '新しいメールアドレス名'}

class UserNameSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)
        labels = {'username': '新しいユーザ名'}

class ImageSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('image',)


# allauthのログインフォーム
class MyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# allauthの登録フォーム
class MySignUpForm(SignupForm):
    image = forms.ImageField()
    class Meta:
        model = User
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        
        self.fields['username'].widget.attrs['placeholder'] = 'ユーザ名の入力'
        self.fields['email'].widget.attrs['placeholder'] = 'emailの入力'
        self.fields['password1'].widget.attrs['placeholder'] = 'パスワードの入力'
        self.fields['password2'].widget.attrs['placeholder'] = 'パスワードの再入力'
    def signup(self, request, user):
        user.icon = self.cleaned_data['icon']
        user.save()
        return user

# allauthのパスワードリセットフォーム（loginからのパスワードのリセット メール送信フォーム）
class MyResetPasswordForm(ResetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


# allauthのパスワードリセットフォーム（loginからのパスワードのリセット 変更用フォーム）
class MyResetPasswordKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['placeholder'] = 'パスワード'
        self.fields['password2'].widget.attrs['placeholder'] = 'パスワード確認用'

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'




