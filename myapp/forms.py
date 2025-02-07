from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
)
from .models import CustomUser
from django.contrib.auth.hashers import check_password
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


class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError("ユーザー名またはパスワードが間違っています。")

        return super().clean()


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


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        fields = ["old_password", "new_password1", "new_password2"]

    def clean(self):
        old_password = self.cleaned_data.get("old_password")
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        current_user = self.user

        if old_password and not check_password(old_password, current_user.password):
            raise forms.ValidationError("旧パスワードが一致しませんでした")

        if old_password == new_password1:
            raise forms.ValidationError("そのパスワードは既に使用しています")

        if new_password1 != new_password2:
            raise forms.ValidationError("新パスワードが一致しません。")

        return super().clean()
