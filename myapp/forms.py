from django import forms
from django.forms import fields
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm

from myapp.models import CustomUser

def clean_image(img):
    '''サインアップ時の画像サイズが大きいとエラーを出す関数'''
    if img:
        if img.size > 2*1024*1024:
            raise ValidationError('ファイルサイズは2MB以下にしてください')
        return img
    else:
        raise ValidationError('画像を読み込めませんでした')

class CustomSignUpForm(SignupForm):
    '''サインアップ用フォーム'''
    image = fields.ImageField(
        required=False,
        label='image',
        validators=[clean_image],
    )

    def save(self, request):
        user = super(CustomSignUpForm, self).save(request)
        return user

    class Meta:
        model = CustomUser


class MessageForm(forms.Form):
    '''新規メッセージ用フォーム'''
    content = forms.CharField(
        label="message", 
        required=True,
        max_length=1000,
        widget=forms.TextInput(
            attrs={
                "class":"form-control",
            }
        )
    )

class UserUpdateForm(forms.Form):
    '''ユーザー情報アップデート用フォーム'''
    username = forms.CharField(
        max_length=30,
        required=True,
        label="Username",
    )
    email = forms.EmailField(
        max_length=100,
        required=True,
        label="Email",
    )
    image = forms.ImageField(
        required=True,
        label="Image",
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'image')