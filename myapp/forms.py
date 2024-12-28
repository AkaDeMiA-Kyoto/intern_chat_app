from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
)
from .models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2", "image")

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image and image.image.format not in ["PNG", "JPG", "JPEG", "PDF"]:
            raise forms.ValidationError(
                "画像の形式は「png」,「jpg」,「pdf」にしてください。"
            )

        return image

    def clean(self):
        username = self.cleaned_data.get("username")
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if username == None:
            raise forms.ValidationError("そのユーザ名は既に使用されています")

        if password1 != password2:
            raise forms.ValidationError("パスワードが一致しません。")

        if username.lower() in password1.lower():
            raise forms.ValidationError(
                "ユーザー名とパスワードが似すぎています。別のパスワードを設定してください。"
            )

        if len(password1) < 8:
            raise forms.ValidationError("パスワードは8文字以上で入力してください。")

        return super().clean()


class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and not CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("指定されたユーザーは存在しません。")

        user = authenticate(self.request, username=username, password=password)
        if user is None:
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

        if "@" not in email or "." not in email:
            raise forms.ValidationError("有効なメールアドレスを入力してください。")
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

        if new_password1 and current_user.username.lower() in new_password1.lower():
            raise forms.ValidationError(
                "ユーザー名とパスワードが似すぎています。別のパスワードを設定してください。"
            )

        if new_password1 and len(new_password1) < 8:
            raise forms.ValidationError("パスワードは8文字以上で入力してください。")

        return super().clean()
