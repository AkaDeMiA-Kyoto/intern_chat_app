from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import SignUpForm


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    """forms.ModelFormを用いたお問い合わせ"""
    if request.method == 'POST':
        # フォーム送信データを受け取る
        form = SignUpForm(request.POST, request.FILES)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = SignUpForm()

    return render(request, 'myapp/signup.html', {'form': form})

def login_view(request):
    return render(request, "myapp/login.html")


class MyLogin(LoginView):
    template_name = "myapp/login.html"
    
def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
