from curses.ascii import SI
import imp
from multiprocessing import context
from django.shortcuts import redirect, render
from .models import CustomUser
from .forms import SignUpForm

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    context = {
        'form' : SignUpForm(),
        'msg' : 'Good',
    }
    if request.method == 'POST':
        obj = CustomUser()
        form = SignUpForm(request.POST,instance = obj)
        if form.is_valid():
            form.save()
            context['form'] = SignUpForm(request.POST)
            return redirect(to='/')
        else:
            context["msg"] = 'bad'
    return render(request, "myapp/signup.html",context)

def login_view(request):
    return render(request, "myapp/login.html")

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
