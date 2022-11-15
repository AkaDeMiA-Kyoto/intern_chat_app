from django.shortcuts import redirect, render,get_object_or_404

from .forms import SignUpForm
from django.contrib.auth.views import LoginView,PasswordChangeView,PasswordChangeDoneView,LogoutView
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView
from . forms import UserCreationForm,LoginForm,TalkForm,PasswordChangeForm,UserNameChangeForm,MailChangeForm,ImageChangeForm
from . models import CustomUser,Talk
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    return render(request, "account/signup.html")

def login_view(request):
    return render(request, "myapp/login.html")


def friends(request):
    user = request.user
    friendsname = CustomUser.objects.exclude(id=user.id)
    
    context = {
        "friends_list":friendsname
    }
    keyword = request.GET.get('keyword')
    if keyword:
        friendsname = friendsname.filter(
            Q(username_icontains=keyword)
        )
    return render(request, "myapp/friends.html",context)

def talk_room(request,user_id):
    user = request.user
    friend = get_object_or_404(CustomUser,id=user_id)
    talk = Talk.objects.filter(Q(talk_from=user,talk_to=friend)|Q(talk_from=friend,talk_to=user))
    form = TalkForm()
    context = {"form":form,"talk":talk,"friend":friend }
    if request.method == "POST":
        new_talk = Talk(talk_from=user,talk_to=friend)
        form = TalkForm(request.POST,instance=new_talk)
        
        if form.is_valid():
            form.save()
            return redirect("talk_room",user_id)
        else:
            print(form.error)

    return render(request, "myapp/talk_room.html",context)

def setting(request):
    return render(request, "myapp/setting.html")

#アカウント作成
def CreateAccount(request):

    if request.method == 'POST':
        print(request.FILES)
        form = SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            print('動きました')
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = SignUpForm()

    return    render(request,'myapp/signup.html',{'form':form})

def username_change(request):
    user = request.user
    if request.method == 'GET':
        form = UserNameChangeForm(instance=user)
    
    elif request.method == 'POST':
        form = UserNameChangeForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('username_change_done')
        else:
            print(form.errors)
    context = {
        "form":form,
    }
    return render(request,"myapp/username.html",context)

def username_change_done(request):
    return render(request,'myapp/username_change_done.html')

def email_change(request):
    user = request.user
    if request.method == 'GET':
        form = MailChangeForm(instance=user)
    
    elif request.method == 'POST':
        form = MailChangeForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('mailchange_done')
        else:
            print(form.errors)
    context = {
        "form":form,
    }
    return render(request,"myapp/mailchange.html",context)

def email_change_done(request):
    return render(request,'myapp/mailchange_done.html')

def icon_change(request):
    user = request.user
    if request.method == 'GET':
        form = ImageChangeForm(instance=user)
    
    elif request.method == 'POST':
        form = ImageChangeForm(request.POST,request.FILES,instance=user,)
        if form.is_valid():
            form.save()
            return redirect('iconchange_done')
        else:
            print(form.errors)
    context = {
        "form":form,
    }
    return render(request,"myapp/iconchange.html",context)

def icon_change_done(request):
    return render(request,"myapp/iconchange_done.html")
class PasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'myapp/password.html'

        


class Account_login(LoginView):
   authentication_form = LoginForm
   template_name = "myapp/login.html"

class Logout(LogoutView,LoginRequiredMixin):
    template_name = "myapp/index.html"
    
class PasswordChangeDone(PasswordChangeDoneView):
    template_name = "myapp/password_change_done.html"





