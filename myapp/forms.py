from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpForm (UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text='必須 有効なメールアドレスを入力してください。',
        label='Eメールアドレス'
    )
    class Meta:
         model = User
         fields = ('email', 'username', 'icon'  )

