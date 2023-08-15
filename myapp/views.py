from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.contrib.auth import login, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import SignUpForm
from django.contrib.auth.forms import UserCreationForm


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            if 'image' in request.FILES:
                user.image = request.FILES['image']
                user.save()
            return redirect('index')
    else:
        form = SignUpForm(request.POST, request.FILES)
    return render(request, "myapp/signup.html", {'form': form})

def login_view(request):
    return render(request, "myapp/login.html")

@login_required
def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")