from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django import forms
from .models import CustomUser, Talk
from allauth.account.forms import SignupForm as AllAuthSignupForm

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2", "img")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

class CustomSignupForm(AllAuthSignupForm):
    img = forms.ImageField(required=True)

    class Meta:
        model = CustomUser

    def signup(self, request, user):
        user.img = self.cleaned_data['img']
        user.save()
        return user

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'

class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ('content',)

class PasswordChangingForm(PasswordChangeForm):
    class Meta:
        model = CustomUser
        fields = ("old_password", "password1", "password2")

class NameChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username",)


class MailChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("email",)

class IconChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("img",)
