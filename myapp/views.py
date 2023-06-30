from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import SignUpForm, LogInForm
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    return render(request, "myapp/signup.html")

def login_view(request):
    return render(request, "myapp/login.html")

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(to = 'index')
    else:
        form = SignUpForm()

    return render(request, "myapp/signup.html", {"form": form})

class FriendsView(LoginRequiredMixin, TemplateView):
    template_name = 'friends.html'
    login_url = '/login/'

class Login(LoginView):
    template_name = 'login.html'
    form_class = LogInForm