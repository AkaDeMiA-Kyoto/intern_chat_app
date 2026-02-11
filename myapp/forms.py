from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    icon = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "icon", "password1", "password2")
        labels = {
            "username": "user_name",
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.image = self.cleaned_data.get("image")
        if commit:
            user.save()
        return user