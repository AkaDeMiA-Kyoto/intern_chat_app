from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.forms import AuthenticationForm

class SingupForm(forms.Form):
    username = forms.CharField(
        label='Username',
        required=True,
        )

    email = forms.EmailField(
        label='Email Address',
        required=True
    )

    password = forms.CharField(
        label='password',
        widget=forms.PasswordInput(),
        min_length=8,
        required=True
    )

    password_confirmation = forms.CharField(
        label='password-confirmation',
        widget=forms.PasswordInput(),
        min_length=8,
        required=True
    )

    image = forms.ImageField(
        label='image',
        required=False
    )

    def clean(self):
        cleaced_data = super().clean()
        password = cleaced_data.get('password')
        password_confirmation = cleaced_data.get('password_confirmation')
        if password != password_confirmation:
            print('Error code:not right password')
            raise forms.ValidationError(_('password-confirmation is not same as password'), code='not right password')  
        
    # バリデーション
    # メールの形式ではない文字がemailフィールドに入力された時 →　完了
    # パスワードと確認に差異が見られた時 →　完了
    # ユーザーネームとパスワードが酷似していた時 → できていない
    # パスワードが8文字未満の時　→　完了

    # 参考
    # https://itc.tokyo/django/form-validation/

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'ユーザーネーム'
        self.fields['password'].label = 'パスワード'

            