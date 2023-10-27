from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from .models import Talk
from allauth.account.forms import(
    LoginForm,
    SignupForm,
    ResetPasswordKeyForm,
    ResetPasswordForm
)

User = get_user_model()

class UserNameSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username",)
        labels = {"username": "新しいユーザー名"}

class ImageSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("icon",)

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
        self.fields['new_password2'].widget.attrs['placeholder'] = '新しいパスワード（確認用）'
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class MyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class MySignupForm(SignupForm):
    icon = forms.ImageField()
    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs['placeholder'] = 'ユーザー名'
        self.fields["email"].widget.attrs['placeholder'] = 'メールアドレス'
        self.fields["password1"].widget.attrs['placeholder'] = 'パスワード'
        self.fields['password2'].widget.attrs['placeholder'] = 'パスワード（確認用）'

        for field in self.fields.values():
            field.widget.attrs["autocomplete"] = "off"
            if field != self.fields['icon']:
                field.widget.attrs['class'] = 'form-control'

    def signup(self, request, user):
        user.icon = self.cleaned_data['icon']
        user.save()
        return user
    
class MyResetPasswordKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].widget.attrs['placeholder'] = 'パスワード（確認用）'
        for field in self.field.values():
            field.widget.attrs['class'] = 'form-control'

class MyResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class FriendsSearchForm(forms.Form):

    keyword = forms.CharField(
        label="検索",
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "ユーザー名またはメールアドレスで検索",
            "autocomplete": "off",
            }
        ),    
    )