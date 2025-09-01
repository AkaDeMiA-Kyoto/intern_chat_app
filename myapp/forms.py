from django import forms
from django.contrib.auth.forms import  AuthenticationForm, UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    image = forms.ImageField(label="アイコン（任意）", required=False)
    
    class Meta:
        model = CustomUser
        fields = ("username", "email", "image")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        
class NameForm(forms.ModelForm):
    class Meta:
        model  = CustomUser
        fields = ['username']
        labels = {'username': 'ユーザ名'}

class EmailForm(forms.ModelForm):
    class Meta:
        model  = CustomUser
        fields = ['email']
        labels = {'email': 'メールアドレス'}

class IconForm(forms.ModelForm):
    class Meta:
        model  = CustomUser
        fields = ['image']
        labels = {'image': 'アイコン画像'}