from django.shortcuts import redirect, render
from .forms import SignupForm, LoginForm
from django.contrib.auth import login


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == 'POST':

        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, 'myapp/index.html')


    else:
        form = SignupForm()
    
    param = {
        'form': form
    }

    return render(request, 'myapp/signup.html', param)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            if user:
                login(request, user)
                return render(request, 'myapp/friends.html')

    else:
        form = LoginForm()

    param = {
        'form': form,
    }

    return render(request, "myapp/login.html", param)

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
