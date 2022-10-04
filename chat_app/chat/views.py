# from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, "chat/index.html")

def login(request):
    return render(request, "chat/login.html")

def signup(signup):
    return render(request, "chat/signup")