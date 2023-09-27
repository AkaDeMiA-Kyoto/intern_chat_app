from .models import CustomUser, Message
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView
from django import forms

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'image')

class LogInForm(AuthenticationForm):
    error_messages = {
            'invalid_login': _(
                "ユーザーID,パスワードが一致しません."
            ),
            'inactive': _(
                "ユーザーが存在しません."
            )
        }

class LogInView(LoginView):
    authentication_form = LogInForm

class MessageForm(forms.ModelForm):
    class Meta():
        model = Message
        fields = ('content',)
        labels = {'content':"本文"}

class ChangeNameForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username',)

class ChangeMailForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

class ChangeIconForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('image',)        