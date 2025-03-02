from django.shortcuts import redirect, render
from .forms import Singup_Form


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    form = Singup_Form()
    return render(request, "myapp/signup.html", {'form' : form})

def login_view(request):
    return render(request, "myapp/login.html")

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")

def signup_form_view(request):
    if request.method == "post":
        form = Singup_Form(request.post)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = Singup_Form()
    return render(request,"myapp/signup.html", {'form': form})
