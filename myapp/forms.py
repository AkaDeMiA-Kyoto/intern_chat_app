from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import CustomUser
class SignUpForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2','image')
class LogInForm(AuthenticationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'password')
