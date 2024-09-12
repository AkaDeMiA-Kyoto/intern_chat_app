from django.shortcuts import render
from .forms import SignupForm

def signup_view(request):
    if request.method == 'POST':

        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()

    else:
        form = SignupForm()
    
    param = {
        'form': form
    }

    return render(request, 'myapp/signup.html', param)


def index(request):
    return render(request, "myapp/index.html")


def login_view(request):
    return render(request, "myapp/login.html")

def user_view(request):
    pass

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")