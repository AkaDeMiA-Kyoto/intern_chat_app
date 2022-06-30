from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model



User = get_user_model()

class SignUpForm (UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text='必須 有効なメールアドレスを入力してください。',
        label='Eメール'
    )
    class Meta:
         model = User
         fields = ( 'email', 'username', 'icon', )

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] ='form-control'
            field.widget.attrs['placeholder'] = field.label

    
