from django.shortcuts import redirect, render
from django.contrib.auth import login
from .forms import SingupForm, LoginForm


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    form = SingupForm()
    if request.method == "GET": 
        return render(request, "myapp/signup.html", {'form' : form})
    if request.method == "POST":
        form = SingupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("myapp:index")
    return render(request,"myapp/signup.html", {'form' : form})

def login_view(request):
    form = LoginForm()
    if request.method == "GET":
        return render(request, "myapp/login.html", {'form' : form})
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("myapp:friends")
    return render(request, "myapp/login.html", {'form' : form})

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")

