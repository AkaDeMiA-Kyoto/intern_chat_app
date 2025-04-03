from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Signup, Message


class SingupForm(UserCreationForm):
    class Meta:
        model = Signup
        fields = ["username", "email", "password1", "password2", "img"]
        error_messages ={
            'username':{'unique': 'このユーザー名は既に使われています。',}
        }
    
    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise ValidationError("パスワードが一致しません。")
        
        if len(password1) < 8:
            raise ValidationError("パスワードは8文字以上です。")
        
        if (username in password1 or password1 in username) and username >= 4:
            raise ValidationError("ユーザーネームとパスワードが酷似しています。")

        return cleaned_data

class LoginForm(AuthenticationForm):
    pass

class MessageSend(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']

class UsernameUpdate(forms.ModelForm):
    class Meta:
        model = Signup
        fields = ['username']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # request を受け取る
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username')

        if self.request:
            user = self.request.user  # 現在のログインユーザー
            password = user.password
            if (username in password or password in username) and len(username) >= 4:
                raise ValidationError("ユーザーネームとパスワードが酷似しています。")
        
        return cleaned_data
    
class EmailUpdate(forms.ModelForm):
    class Meta:
        model = Signup
        fields = ['email']

class PasswordUpdate(forms.ModelForm):
    current_password = forms.CharField(widget=forms.PasswordInput,max_length=100, required=True, label="現在のパスワード") 

    class Meta:
        model = Signup
        fields = ['current_password',"password1","password2",]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('user', None)  # request を受け取る
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError("パスワードが一致しません。")
        
        if len(password1) < 8:
            raise ValidationError("パスワードは8文字以上です。")

        if self.request:
            current_password = cleaned_data.get('current_password')
            user = self.request.user  # 現在のログインユーザー
            username = user.username
            password = user.password1
            if (username in password1 or password1 in username) and len(username) >= 4:
                raise ValidationError(f"ユーザーネームとパスワードが酷似しています。{password}")
            if password != current_password:
                raise ValidationError("現在のパスワードが違います。")
        
        return cleaned_data
    
class ImgUpdate(forms.ModelForm):
    class Meta:
        model = Signup
        fields = ['img']