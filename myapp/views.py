from django.shortcuts import redirect, render
from .models import CustomUser


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    return render(request, "myapp/signup.html")

def login_view(request):
    return render(request, "myapp/login.html")

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")

def register(request):
    CustomUser.objects.create(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'], icon_image=request.FILES['image'])
    return redirect('index')
