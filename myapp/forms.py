from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Talk
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm


class SignUpForm(UserCreationForm):
    class Meta:
        model= CustomUser
        fields = ('username', 'email','image',) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'email','password1','password2',]:
            self.fields[fieldname].help_text = None

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class TalkForm(forms.ModelForm):
    class Meta:
        model =Talk
        fields = ('talk',)

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model= CustomUser
        fields = ('username',) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs.get('instance', None)
        self.fields['username'].widget.attrs['value'] = 'username'

class MailChangeForm(forms.ModelForm):
    class Meta:
        model= CustomUser
        fields = ('email',) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs.get('instance', None)
        self.fields['email'].widget.attrs['value'] = 'email'

class ImageChangeForm(forms.ModelForm):
    class Meta:
        model= CustomUser
        fields = ('image',) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs.get('instance', None)
        self.fields['image'].widget.attrs['value'] = 'image'

class PasswordChangeForm(PasswordChangeForm):
    pass