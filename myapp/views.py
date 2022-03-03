from operator import imod
from pipes import Template
from unicodedata import name
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import HelloForm


def index(request):
    return render(request, "myapp/index.html")

class HelloView(TemplateView):

    def __init__(self):
        self.params = {
            'title': 'Hello',
            'message': '',
            'form': HelloForm()
        }
    
    def get(self, request):
        return render(request, 'myapp/signup.html', self.params)
    
    def post(self, request):
        msg = 'Username: ' + request.POST['username']+ \
            '<br>Emailaddress: ' + request.POST['emailaddress'] + \
            '<br>Password: ' + request.POST['password'] + \
            '<br>Password Confirmation: ' +request.POST['passwordconfirmation'] + \
            '<br>img: ' + request.POST['img'] 
        self.params['message'] = msg
        self.params['form'] = HelloForm(request.POST)
        return render(request, 'myapp/signup.html', self.params)


def login_view(request):
    return render(request, "myapp/login.html")

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")


