from django.forms import ModelForm
from .models import Signup


class Singup_Form(ModelForm):
    class Meta:
        model = Signup
        fields = ["username", "email", "password1", "password2", 'image']
