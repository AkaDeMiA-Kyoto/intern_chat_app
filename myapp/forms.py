from django import forms
from allauth.account.forms import SignupForm
from .models import CustomUser, Message

class CustomSignupForm(SignupForm):
    email = forms.EmailField(label='Email')
    img = forms.ImageField(label='Img')

    def signup(self, request, user):
        user.save()
        return user


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class':'form-control form-control-sm', 'rows':2})
        }


class UsernameChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomUser
        fields = ('username',)


class UsermailChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomUser
        fields = ('email',)


class UsericonChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['img'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomUser
        fields = ('img',)