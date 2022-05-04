from django.shortcuts import render,redirect
from allauth.account import views

class LoginView(views.LoginView):
    template_name = 'account/login.html'


class LogoutView(views.LogoutView):
    template_name = 'account/signup.html'

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.logout()
        return redirect('/')


class SignUpView(views.SignupView):
    template_name = 'account/signup.html'
