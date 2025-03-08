from django.shortcuts import redirect, render
from .forms import Singup_Form


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    form = Singup_Form()
    if request.method == "GET": 
        return render(request, "myapp/signup.html", {'form' : form})
    if request.method == "POST":
        form = Singup_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("myapp:index")
    return render(request,"myapp/signup.html", {'form': form})

def login_view(request):
    return render(request, "myapp/login.html")

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")

