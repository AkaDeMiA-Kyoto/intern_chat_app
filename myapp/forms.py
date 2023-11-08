from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import CustomUser

CustomUser = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
             "email",
             "image",
             "password1",
             "password2",
             )