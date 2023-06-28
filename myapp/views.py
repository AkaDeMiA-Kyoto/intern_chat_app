from django.shortcuts import redirect, render
from .forms import SignUpForm
from django.views.generic.edit import CreateView
from .models import CustomUser
from django.urls import reverse_lazy

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    return render(request, "myapp/signup.html")

def login_view(request):
    return render(request, "myapp/login.htmls")

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")

class SignUpView(CreateView):
    template_name="myapp/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy('index')
