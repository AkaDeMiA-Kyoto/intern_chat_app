from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import HelloForm
from .forms import PhotoForm
from .forms import SignUpForm, MessageForm, NameForm, emailchangeForm, passwordchangeForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from django.views import generic
from .forms import LoginForm
from .models import Photo, Message
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse


def index(request):
    params = {
        'title':'ログイン',
        'msg':'login',
        'gotoo':'login_view',
        'goto':'signup_view'
    }
    return render(request, "myapp/index.html", params)


def signup_view(request):
    params = {
    'form1': SignUpForm(),
    'form2': PhotoForm(),
    } 
    if (request.method == 'POST'):
        form1 = SignUpForm(request.POST)
        form2 = PhotoForm(request.POST, request.FILES)
        if form1.is_valid():
            user = form1.save()
        else:
            params['form1'] = form1
            return render(request, "myapp/signup.html", params)
        if form2.is_valid():
            form2.save(commit = False)
            form2.instance.username = user
            form2.save()
        else:
            print(form2.errors)
            
        username = form1.cleaned_data.get('username')
        raw_password = form1.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(request, user)
        return redirect('index')
    else:
        form1 = SignUpForm()
        form2 = PhotoForm()
           
    return render(request, "myapp/signup.html", params)
# def login_view(request):
    
#     return render(request, "myapp/login.html")
def friends(request):   
    user = request.user
    data = User.objects.exclude(username=user.username)
    print(User.objects.exclude(username=user.username))
    message = Message.objects.all().order_by('pub_date').reverse()
    photo = Photo.objects.all()
    params = {
                'data': data,
                'photo': photo,
                'message': message,
                }


    return render(request, "myapp/friends.html", params)

def talk_room(request, tousername):
    print(request.user)
    user = request.user

    data7 = User.objects.get(id=user.id)
    data5 = User.objects.get(username=tousername)
    fromusername = data7.username
    print(tousername)
    if (request.method == 'POST'):
        user2 = User.objects.get(id=user.id)
        user1 = User.objects.get(username=tousername)
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit = False)
            form.instance.tousername = user1
            form.instance.fromusername = user2
            form.save()
        else:
            params['form'] = form
            return render(request, 'talk_room', params)
    date = Message.objects.all().reverse()

    try:
        data6 = Message.objects.filter(Q(tousername__username=tousername, fromusername__username=fromusername) | Q(tousername__username=fromusername, fromusername__username=tousername))
    except Message.DoesNotExist:
        data6 = None
    params = {
        'messageform': MessageForm(),
        'data6': data6,
        'abc': '送信',
        'def': '受信',
        'data5': tousername
    }

    return render (request, "myapp/talk_room.html", params)

def setting(request):
    data = request.user
    params = {
        'data': data
    }
    return render(request, "myapp/setting.html", params)

def usernameok(request):
    params = {
        'body': 'ユーザ名変更完了'
    }
    return render(request, "myapp/usernameok.html", params)



class Login(LoginView):
    """ログインページ"""

    authentication_form = LoginForm

    template_name = 'myapp/login.html'
    

class Logout(LoginRequiredMixin, LogoutView):
    pass
def usernamechange(request, fromusername):
    
    obj = User.objects.get(username=fromusername)
    params = {
        'form': NameForm(instance=obj),
        'obj': obj,
    }

    if (request.method == 'POST'):

        form = NameForm(request.POST, request.FILES, instance=obj)

        if form.is_valid():
            form.save()

        else:
            print(form.errors)
            params['form'] = form

            return render(request, 'myapp/usernamechange.html', params)

        return redirect('usernameok')
        
    return render(request, "myapp/usernamechange.html", params)

def emailchange(request, fromusername):
    
    obj = User.objects.get(username=fromusername)
    params = {
        'form': emailchangeForm(instance=obj),
        'obj': obj,
    }

    print(obj)
    if (request.method == 'POST'):

        form = emailchangeForm(request.POST, request.FILES, instance=obj)

        if form.is_valid():
            form.save()

        else:
            print(form.errors)
            params['form'] = form

            return render(request, 'myapp/emailchange.html', params)

        return redirect('emailok')
        
    return render(request, "myapp/emailchange.html", params)

def emailok(request):
    params = {
        'body': 'メールアドレス変更完了'
    }
    return render(request, "myapp/emailok.html", params)

def passwordchange(request, fromusername):
    
    obj = User.objects.get(username=fromusername)
    params = {
        'form': passwordchangeForm(instance=obj),
        'obj': obj,
    }
    print(obj)
    if (request.method == 'POST'):
        print('iuyi')
        form = passwordchangeForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
            params['form'] = form
            return render(request, 'myapp/passwordchange.html', params)
        return redirect('passwordok')
        
    return render(request, "myapp/passwordchange.html", params)


def passwordok(request):
    params = {
        'body': 'パスワード変更完了'
    }
    return render(request, "myapp/passwordok.html", params)

def iconchange(request, fromusername):
    
    obj = User.objects.get(username=fromusername)
    params = {
        'form': PhotoForm(instance=obj),
        'obj': obj,
    }
    print(obj)
    if (request.method == 'POST'):
        form = PhotoForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            user_image = Photo.objects.get(username = request.user)
            user_image.image = request.FILES["image"]
            user_image.save()
        else:
            print(form.errors)
            params['form'] = form
            return render(request, 'myapp/iconchange.html', params)
        return redirect('iconok')
        
    return render(request, "myapp/iconchange.html", params)

def iconok(request):
    params = {
        'body': 'アイコン変更完了'
    }
    return render(request, "myapp/iconok.html", params)











