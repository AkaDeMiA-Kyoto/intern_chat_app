from django import forms
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254
        label='Emailadress'
    )
    img = forms.ImageField(
        upload_to='MEDIA_ROOT'
        label='img'
    )
    class Meta:
        model = AbstractUser
        fields = ('Username','Emailadress','password1','password2','image')
