from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth import authenticate


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2", "image")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if "@" not in email or "." not in email:
            raise forms.ValidationError("有効なメールアドレスを入力してください。")
        return email

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
    
