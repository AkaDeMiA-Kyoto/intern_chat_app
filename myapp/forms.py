from django.forms import ModelForm
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 



class SignUpForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email','password1', 'password2', 'image')

    
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label   


