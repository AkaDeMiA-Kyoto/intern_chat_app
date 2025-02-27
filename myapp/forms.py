from django import forms
from .models import CustomUser
from allauth.account.forms import SignupForm
from django.core.validators import FileExtensionValidator


class CustomSignupForm(SignupForm):
    image = forms.ImageField(required=False, label="プロフィール画像")

    def save(self, request):
        user = super().save(request)
        image = self.cleaned_data.get("image")
        user.image = image
        user.save()
        return user


class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username"]


class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["email"]


class ImageChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["image"]

    image = forms.ImageField(
        required=False,
        label="プロフィール画像",
        validators=[
            FileExtensionValidator(allowed_extensions=["png", "jpg", "jpeg", "pdf"])
        ],
    )
