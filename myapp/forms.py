from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password

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
    # 【保存版】Djangoフォームでバリデーションを実装する方法 https://itc.tokyo/django/form-validation/

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'ユーザーネーム'
        self.fields['password'].label = 'パスワード'

class MessageForm(forms.Form):
    talk_room_id = forms.CharField(
        max_length=100,
        widget=forms.HiddenInput()
        )
    user_id = forms.CharField(
        max_length=100,
        widget= forms.HiddenInput()
    )
    friend_id = forms.CharField(
        max_length=100,
        widget= forms.HiddenInput()
    )
    content = forms.CharField(
        max_length=1000,
        required=True,
        )

class NameChangeForm(forms.Form):
    # 入力してもらう確認用パスワード
    current_password = forms.CharField(
        label='Current password',
        widget=forms.PasswordInput(),
        min_length=8,
        required=True
    )

    changed_inf = forms.CharField(
    max_length=100,
    widget= forms.HiddenInput(),
    initial='name'
    )

    new_username = forms.CharField(
    label='New username',
    required=True,
    )

    # 正しいパスワード
    old_password_data = forms.CharField(
        widget=forms.HiddenInput(),
        min_length=8,
        required=True
    )

    # passwordが正しいか確認する
    def clean(self):
        cleaced_data = super().clean()
        if not check_password(cleaced_data.get('current_password'), cleaced_data.get('old_password_data')):
            print('Error code:not right password')
            raise forms.ValidationError(_('current_password is wrong'), code='not right password')  


class EmailChangeForm(forms.Form):
    current_password = forms.CharField(
        label='Current password',
        widget=forms.PasswordInput(),
        min_length=8,
        required=True
    )

    changed_inf = forms.CharField(
    max_length=100,
    widget= forms.HiddenInput(),
    initial='email'
    )

    new_email = forms.EmailField(
        label='New Email Address',
        required=True
    )

    # 正しいパスワード
    old_password_data = forms.CharField(
        widget=forms.HiddenInput(),
        min_length=8,
        required=True
    )

    # passwordが正しいか確認する
    def clean(self):
        cleaced_data = super().clean()
        if not check_password(cleaced_data.get('current_password'), cleaced_data.get('old_password_data')):
            print('Error code:not right password')
            raise forms.ValidationError(_('current_password is wrong'), code='not right password')  

class IconChangeForm(forms.Form):
    current_password = forms.CharField(
        label='Current password',
        widget=forms.PasswordInput(),
        min_length=8,
        required=True
    )

    changed_inf = forms.CharField(
    max_length=100,
    widget= forms.HiddenInput(),
    initial='icon'
    )

    new_image = forms.ImageField(
        label='New image',
        required=False
    )

    # 正しいパスワード
    old_password_data = forms.CharField(
        widget=forms.HiddenInput(),
        min_length=8,
        required=True
    )

    # passwordが正しいか確認する
    def clean(self):
        cleaced_data = super().clean()
        if not check_password(cleaced_data.get('current_password'), cleaced_data.get('old_password_data')):
            print('Error code:not right password')
            raise forms.ValidationError(_('current_password is wrong'), code='not right password')  


# 参考
# 【Django】Formに初期値を設定 4つの方法をまとめました https://itc.tokyo/django/form-with-initial-value/
            