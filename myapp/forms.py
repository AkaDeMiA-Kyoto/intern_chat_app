from django.forms import ModelForm
from django import forms
from .models import CustomUser, TalkLog
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm



class SignUpForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email','password1', 'password2', 'image')

    
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label   

class ChatMessageForm(forms.Form):
    message = forms.CharField(label='', max_length=100, required=True )


class ChangeNameForm(forms.Form):
    username = forms.CharField(label='Username', max_length=15, required=True)


class ChangeMailForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=50, required=True)

class ChangeIconForm(forms.Form):
    image = forms.ImageField(label='Image', required=True)

# class ChangePasswordForm(forms.Form):
#     password1 = forms.CharField(label='Password', max_length=30, required=True)
#     password2 = forms.CharField(label='Password confirmation', max_length=30, required=True)

# class ChangePasswordForm(PasswordChangeForm):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['new_password1'].help_text = "8文字以上のパスワードを設定してください"
#         self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
#         self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})
