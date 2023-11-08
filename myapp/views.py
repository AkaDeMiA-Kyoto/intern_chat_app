from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .forms import CreateUserForm

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == 'POSt':
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username, password)
            if user is not None:
                login(request, user)
            return redirect("/")
        else:
            print(form.errors)
    else:
        form = CreateUserForm()
    context = {
        "form": form,
    }
    return render(request, "myapp/signup.html", context)

def login_view(request):
    return render(request, "myapp/login.html")

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
