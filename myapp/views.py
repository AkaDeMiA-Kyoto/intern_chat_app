from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "myapp/index.html")


def signup_view(request):
    return render(request, "myapp/signup.html")


def login_view(request):
    return render(request, "myapp/login.html")


@login_required
def friends(request):
    return render(request, "myapp/friends.html")


def talk_room(request):
    return render(request, "myapp/talk_room.html")


def setting(request):
    return render(request, "myapp/setting.html")
