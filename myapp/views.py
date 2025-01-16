from django.shortcuts import redirect, render
from django.contrib.auth import login,authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from .forms import SignUpForm, LogInForm

class IndexView(TemplateView):
    template_name = "myapp/index.html"

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'myapp/signup.html'
    get_success_url = reverse_lazy("myapp:index")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
class CustomLoginView(LoginView):
    form_class = LogInForm
    template_name = 'myapp/login.html'
    #LoginViewのsuccess_urlはデフォルトで定義されてないので、settings.pyに記述

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        """
        ログイン失敗時の処理
        """
        return super().form_invalid(form)

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
