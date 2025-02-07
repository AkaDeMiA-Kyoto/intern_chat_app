from django import forms
from .models import CustomUser
from allauth.account.forms import SignupForm
from django.core.validators import validate_email
from allauth.account.models import EmailAddress


class CustomSignupForm(SignupForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "image", "password1", "password2")

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

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise forms.ValidationError("ユーザ名を入力してください")

        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("このユーザー名は既に使用されています。")

        return username


class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["email"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("メールアドレスを入力してください")

        try:
            validate_email(email)
        except forms.ValidationError as e:
            raise forms.ValidationError("無効なメールアドレスです: " + str(e))

        if EmailAddress.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスはすでに使用されています。")

        return email


class ImageChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["image"]

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image and image.image.format not in ["PNG", "JPG", "JPEG", "PDF"]:
            raise forms.ValidationError(
                "画像の形式は「png」,「jpg」,「pdf」にしてください。"
            )

        return image
