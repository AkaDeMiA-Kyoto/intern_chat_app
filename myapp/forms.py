from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import(
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm,
    UserChangeForm
)

from .models import CustomUser, Talk
# forms.pyは何かを送信するときに使う(request.post の便利ver)
# 黄色は関数
# ()をつけると関数に引数を入れずに呼び出して、結果がそこに返ってくる
User = get_user_model()
#User = get_user_model()
class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "img")

class LogInForm(AuthenticationForm):
    template_name = 'myapp/login.html'
    success_url = 'myapp.friends.html'

class TalkForm(forms.ModelForm):
    # トーク送信のためのform
    # メッセージを送信するだけで、誰から誰か、時間はすべて自動で対応できるのでこれだけで十分

    class Meta:
        model = Talk
        fields = ('talk',)
        # 入力予測の表示をさせない(めっちゃ邪魔)
        widgets = {"talk": forms.TextInput(attrs={"autocomplete": "off"})}

class ChangeEmailForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

    password = forms.CharField(widget=forms.HiddenInput(), required=False)
    password1 = forms.CharField(widget=forms.HiddenInput(), required=False)
    password2 = forms.CharField(widget=forms.HiddenInput(), required=False)


class ChangeUsernameForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username',)

    password = forms.CharField(widget=forms.HiddenInput(), required=False)
    password1 = forms.CharField(widget=forms.HiddenInput(), required=False)
    password2 = forms.CharField(widget=forms.HiddenInput(), required=False)

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        # これにより、プロフィール画像 (img) フィールドだけがフォームに表示され、編集可能になります。
        fields = ('img',)

# フォームのメタ情報（Meta Information）は、Djangoのフォームクラス内で使用されるクラスで、フォームの振る舞いや設定に関する情報を指定するための特別なクラスです。Metaクラスは、フォームがどのモデルと関連付けられているか、どのフィールドを含めるか、表示順序などの情報を提供します。主な目的は、フォームの動作をカスタマイズするために使用されます。

# フォームのMetaクラスは通常、以下の属性を持つことがあります：

# model: フォームが関連付けられているデータベースモデルを指定します。
# これにより、フォームがモデルのフィールドと同期し、モデルインスタンスとのデータのやり取りが簡単になります。

# fields: フォームに表示するフィールドを指定します。
# この属性に指定されたフィールドのみがフォームに表示され、ユーザーが入力できます。フィールドはタプルやリストで指定されます。

# exclude: 特定のフィールドをフォームから除外します。fields と併用することはできません。
# exclude に指定されたフィールドはフォームに表示されません。

# widgets: フォームの各フィールドに対してウィジェットを指定します。
# ウィジェットはフィールドの表示方法をカスタマイズするために使用されます。

# その他の属性: さまざまなフォーム設定をカスタマイズするための他の属性も指定できます。
# 例えば、フォームのラベル、ヘルプテキスト、CSSクラスなどを指定できます。

# Metaクラスを使用することで、Djangoフォームをモデルと連携させ、データベースモデルのフィールドを基にフォームを自動生成することができます。
# これにより、フォームとモデル間の整合性を保ちながら、簡単にデータの入力・編集フォームを作成できます。