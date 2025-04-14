from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 

CustomUser = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 
                  'email', 
                  'password1', 
                  'password2', 
                  'user_icon'
                ]
        
class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        
class SettingForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username']
        
class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email']        

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not '@' in email:
            raise forms.ValidationError("有効なメールアドレスを入力してください")
        return email
    
class ImageChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['user_icon']        

    def clean_user_icon(self):
        user_icon = self.cleaned_data.get('user_icon')
        if '/' in  str(user_icon):
            raise forms.ValidationError("画像を選択してください")
        return user_icon