from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from .forms import SignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("index")
    else:
        form = SignUpForm()
    return render(request, "myapp/signup.html", {"form": form})

class Login(LoginView):
    template_name = "myapp/login.html"

class Friends(LoginRequiredMixin, TemplateView): # LoginRequiredMixin はログインを必須にするためのもの
    template_name = "myapp/friends.html"
    login_url = "login"

class TalkRoom(LoginRequiredMixin, TemplateView):
    template_name = "myapp/talk_room.html"
    login_url = "login"

class Setting(LoginRequiredMixin, TemplateView):
    template_name = "myapp/setting.html"
    login_url = "login"
