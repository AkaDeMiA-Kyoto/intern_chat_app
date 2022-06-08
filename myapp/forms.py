from   django import froms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class signup_form (UserCreationForm):
    class meta:
         model = User
         fields = ("username", "email", "icon")

