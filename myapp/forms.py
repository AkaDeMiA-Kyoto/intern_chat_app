from django import forms
from django.contrib.auth import get_user_model

from .models import Talk

User = get_user_model()




class TalkForm(forms.ModelForm):
    """トークの送信のためのform
    メッセージを送信するだけで、誰から誰か、時間は全て自動で対応できるのでこれだけで十分
    """

    class Meta:
        model = Talk
        fields = ("talk",)
        # 入力予測の表示をさせない（めっちゃ邪魔）
        widgets = {"talk": forms.TextInput(attrs={"autocomplete": "off"})}

class UserNameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username",)
        labels = {"username": "新しいユーザ名"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = "form-control"
            field.widget.attrs['placeholder'] = "150 characters or fewer. Letters, digits and @/./+/-/_ only."


class ImageChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("icon",)
        labels = {"icon": "新しいアイコン画像"}
        
