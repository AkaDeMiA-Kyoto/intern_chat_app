from cProfile import label
from dataclasses import field
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    ##email=forms.EmailField(max_length=254,label='メールアドレス')
    ##prof_img=forms.FileField(label='プロフィール画像')
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
    class Meta:
        model=CustomUser
        fields = ['username','email','prof_img',]

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label


class MessageForm(forms.Form):
    content=forms.CharField(label='content',max_length=144)

class SearchForm(forms.Form):
    content=forms.CharField(label='content',max_length=144,required=False)

class ProfImageForm(forms.ModelForm):
    #content=forms.ImageField(label='content')
    class Meta:
        model=CustomUser
        fields=('prof_img',)

class UserNameForm(forms.ModelForm):
    #content=forms.ImageField(label='content')
    class Meta:
        model=CustomUser
        fields=('username',)


