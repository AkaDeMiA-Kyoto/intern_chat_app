from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm



class CustomUserCreationForm(UserCreationForm): 
    # Djangoが提供しているUserCreationFormというformを使う
    # forms.ModelFormと形式が同じで、モデルに基づいたフォームを作ってくれる
    class Meta: #class Metaを書いておけば、Djangoがフォームを作るときに必要な情報を簡単に渡してくれる
        model = CustomUser # 使用するmodelを指定
        fields = ('username', 'email', 'password1', 'password2', 'Img') 
    
    def __init__(self, *args, **kwargs): #注意書きを消す
        super().__init__(*args, **kwargs)
        # super関数・・・上書きしてしまったスーパークラスのメソッドのアトリビュートを使えるようにできる　/　「super().メソッド名(self無し)」
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

class LoginForm(AuthenticationForm):
    # AuthenticationFormはログイン用のフォームクラス
    # usernameとpasswordの2つのフィールドを持つ
    pass

class Username_UpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser # 使用するmodelを指定
        # 表示するフォームを指定
        fields = ('username',) 

class Email_UpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser # 使用するmodelを指定
        # 表示するフォームを指定
        fields = ('email',) 

class Img_UpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser # 使用するmodelを指定
        # 表示するフォームを指定
        fields = ('Img',) 