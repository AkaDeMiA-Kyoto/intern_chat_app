from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .forms import SignUpForm

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        print("check3")
        if form.is_valid():
            print("check1")
            form.save()
            return redirect("index")
        else:
            print(form.errors)
    else:
            form = SignUpForm()
    context = {
        "form": form,
    }
    print("check2")
    return render(request, "myapp/signup.html", context)

def login_view(request):
    return render(request, "myapp/login.html")

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
