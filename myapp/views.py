from django.shortcuts import redirect, render
from .models import CustomUser
from .forms import SignUpForm, LoginForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    return render(request, "myapp/index.html")

class login_view(LoginView,LoginRequiredMixin):
    form_class = LoginForm
    template_name = "myapp/login.html"

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")

def signup_view(request):
    if request.method=='POST':
        form = SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = SignUpForm()

    return render(request,"myapp/signup.html",{'form':form})
