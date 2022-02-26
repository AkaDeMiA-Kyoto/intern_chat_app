from unicodedata import name
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import HelloForm


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    params = {
        'title':'hello',
        'message':'',
        'form': HelloForm()
    }
    if (request.method == 'POST'):
        params['message'] = 'Username: ' + request.POST['username']+ \
            '<br>Emailaddress: ' + request.POST['emailaddress'] + \
            '<br>Password: ' + request.POST['password'] + \
            '<br>Password Confirmation: ' +request.POST['passwordconfirmation'] + \
            '<br>img: ' + request.POST['img']          
        params['form'] = HelloForm(request.POST)
    return render(request, 'myapp/signup.html', params) 

def login_view(request):
    return render(request, "myapp/login.html")

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")


