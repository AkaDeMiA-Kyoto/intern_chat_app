from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm

from allauth.account.forms import ( 
    LoginForm, 
    SignupForm, 
    ResetPasswordKeyForm, 
    ResetPasswordForm
)


from .models import Talk
 
User = get_user_model()


class UserNameSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username",)


class ImageSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("icon",)


class PasswordChangeForm(PasswordChangeForm):
    """Django 標準パスワード変更フォーム

    Djangoはユーザモデルに未加工の (単なるテキストの) パスワードは保存せずハッシュ値でのみ保存する。
    したがって、正しく理解しないとユーザのパスワード属性を直接操作できない。
    よってパスワード編集のために標準で用意されているformを使う。
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['placeholder'] = '元のパスワード'
        self.fields['new_password1'].widget.attrs['placeholder'] = '新しいパスワード'
        self.fields['new_password2'].widget.attrs['placeholder'] = '新しいパスワード(確認用)'
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class TalkForm(forms.ModelForm):
    """トークの送信のためのform

    メッセージを送信するだけで、誰から誰か、時間は全て自動で対応できるのでこれだけで十分
    """

    class Meta:
        model = Talk
        fields = ("talk",)
        # 入力予測の表示をさせない（めっちゃ邪魔）
        widgets = {"talk": forms.TextInput(attrs={"autocomplete": "off"})}


class FriendsSearchForm(forms.Form):
    """友達の中から任意のユーザーを検索"""

    keyword = forms.CharField(
        label="検索",
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "ユーザー名で検索",
            "autocomplete": "off"}),
    )


# allauth ログイン用フォーム
class MyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


# allauth サインアップ用フォーム
class MySignupForm(SignupForm):
    """ Userクラス用フォーム """
    icon = forms.ImageField()
    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # プレースホルダー(フォームの中に入れるガイドの文字)を設定できる
        self.fields['username'].widget.attrs['placeholder'] = 'ユーザー名'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレス'
        self.fields['password1'].widget.attrs['placeholder'] = 'パスワード'
        self.fields['password2'].widget.attrs['placeholder'] = 'パスワード(確認用)'

        # for で回して各フォームに設定を追加できる
        for field in self.fields.values():
            field.widget.attrs["autocomplete"] = "off"
            if field != self.fields['icon']:
                field.widget.attrs['class'] = 'form-control'
    
    def signup(self, request, user):
        user.icon = self.cleaned_data['icon']
        user.save()
        return user

# login でのパスワードリセット(変更用フォーム)
class MyResetPasswordKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].widget.attrs['placeholder'] ='パスワード(確認用)'
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# login でのパスワードリセット(メール送信用フォーム)
class MyResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

