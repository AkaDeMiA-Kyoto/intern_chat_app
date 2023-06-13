from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.forms import ModelForm
from .models import CustomUser, Message

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True
    )
    image = forms.ImageField(
        label="Image",
        required=True
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label="Password(again)",
        widget=forms.PasswordInput()
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "image", "password1", "password2")

class LoginForm(AuthenticationForm):
    pass

class MessageForm(ModelForm):
    message = forms.CharField(
        max_length=500,
        required=True,
        label=""
    )

    class Meta:
        model = Message
        fields = ("message",)

        error_messages = {
            "message": {
                "max_length": "Max 500 letters."
            }
        }

class ChangeUsernameForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
    class Meta:
        model = CustomUser
        fields = ["username"]

class ChangeEmailForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
    class Meta:
        model = CustomUser
        fields = ["email"]

class ChangeImageForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = True
    
    def save(self, user,  *args, **kwargs):
        user = CustomUser.objects.get(pk=user.id)
        if user.image:
            user.image.delete(save=False)
        super(UserChangeForm, self).save(*args, **kwargs)
    
    class Meta:
        model = CustomUser
        fields = ["image"]


