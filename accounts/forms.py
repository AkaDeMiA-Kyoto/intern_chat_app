from allauth.account.forms import SignupForm,LoginForm
from django import forms
from django.contrib.auth import get_user_model
from allauth.account.adapter import DefaultAccountAdapter

Profile = get_user_model()

class SignUpForm(SignupForm):

    image = forms.ImageField()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            print(field)

        self.fields["username"].widget.attrs.update({
            'class':"shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
            'placeholder':""
        })
        self.fields["email"].widget.attrs.update({
            'class':"shadow appearance-none border border-red-500 rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline",
            'placeholder':""
        })
        self.fields["password1"].widget.attrs.update({
            'class':"shadow appearance-none border border-red-500 rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline",
            'placeholder':""
        })
        self.fields["password2"].widget.attrs.update({
            'class':"shadow appearance-none border border-red-500 rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline",
            'placeholder':""
        })
    
    def signup(self, request,user):
        user.image = self.cleaned_data['image']
        user.save()
        return user

    class Meta:
        model = Profile

# class LoginForm(LoginForm):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             print(field)
#             field.widget.attrs['class'] = 'form-control'