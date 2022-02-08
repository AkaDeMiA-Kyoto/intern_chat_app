from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from accounts.models import Profile
from .models import Message

class MessageForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["content"].widget.attrs.update({
            'class':"shadow border-gray-500 border rounded w-full py-2 px-3 text-black leading-tight focus:outline-none focus:shadow-outline",
            'placeholder':""
        })

    class Meta:
        model=Message
        fields=['content']

class UsernameChangeForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["username"].widget.attrs.update({
            'class':"shadow appearance-none border rounded w-full py-2 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
            'placeholder':""
        })
    
    class Meta:
        model=Profile
        fields = ['username']


class UserEmailChangeForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["email"].widget.attrs.update({
            'class':"shadow appearance-none border rounded w-full py-2 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline",
            'placeholder':""
        })
    
    class Meta:
        model=Profile
        fields = ['email']


class UserImageChangeForm(forms.ModelForm):  
    class Meta:
        model=Profile
        fields = ['image']


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs['class'] = "shadow appearance-none border rounded w-full py-2 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
        self.fields['new_password2'].widget.attrs['class'] = "shadow appearance-none border rounded w-full py-2 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
        self.fields['old_password'].widget.attrs['class'] = "shadow appearance-none border rounded w-full py-2 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"