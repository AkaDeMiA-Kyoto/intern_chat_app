from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):

    class Meta:
        model = user
        fields = ('username', 'email', 'password', 'passwordconfirm', 'img')
