from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from.models import CustomUser,Talkroom
from django.utils import timezone



class SignupForm(UserCreationForm):
    username=forms.CharField(label="Username:")
    email=forms.EmailField(label="Emailaddress:")
    img=forms.ImageField(label="Img:",required=False)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "img")

class LoginForm(AuthenticationForm):
    pass


class TalkroomForm(forms.ModelForm):
    class Meta:
        model = Talkroom
        fields = ['message']
        widgets = {
            'content': forms.Textarea()
        }


class Setting_name(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomUser
        fields = ('username',)

class Setting_img(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['img'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomUser
        fields = ('img',)

class Setting_mail(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomUser
        fields = ('email',)

class Setting_password(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomUser
        fields = ('password',)
        

