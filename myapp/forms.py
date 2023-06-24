from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.forms import ModelForm
from allauth.account.forms import SignupForm
from .models import CustomUser, Message

class CustomSignupForm(SignupForm):
    image = forms.ImageField(
        label="プロフィール画像",
        required=True
    )

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.image = request.FILES.get("image")
        user.save()
        return user

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ("message",)
        # 入力予測の表示をさせない
        widgets = {"message": forms.TextInput(attrs={"autocomplete": "off"})}

class ChangeUsernameForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username"]

class ChangeEmailForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ["email"]

class ChangeImageForm(ModelForm):
    def save(self, user,  *args, **kwargs):
        user = CustomUser.objects.get(pk=user.id)
        if user.image:
            user.image.delete(save=False)
        super().save(*args, **kwargs)
    
    class Meta:
        model = CustomUser
        fields = ["image"]


