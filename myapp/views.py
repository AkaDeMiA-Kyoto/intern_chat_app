from datetime import datetime
from time import timezone
from urllib import request
from django.shortcuts import redirect, render 
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import View , generic
from django.views.generic.edit import CreateView
from django.views.generic import FormView
from django import forms
from . import forms 
from myapp.models import CustomUser, TalkContent
from .forms import LoginForm, SignUpForm, UsernameChangeForm ,EmailChangeForm,IconChangeForm,InquiryForm
from django.contrib.auth.views import LoginView ,LogoutView ,PasswordChangeView
from django.utils import timezone
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    return render(request, "myapp/index.html")

class Login (LoginView):
    form_class = LoginForm
    template_name = 'myapp/login.html'

def friends(request):
    friend_list = CustomUser.objects.all()#exclude(request.user)#excludeで自分消す
    return render(request, "myapp/friends.html",context={'friend_list':friend_list})

# class Friendslist(generic.ListView,LoginRequiredMixin):
#     model =CustomUser
#     template_name  = 'myapp/friends.html'
#     def get_queryset(self):
#         friends_list = CustomUser.objects.exclude(id =self.request.user.id)
#         return friends_list

def talk_room(request, Customuser_id):
    if request.method == "POST":
        form = forms.TalkForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.date = timezone.now()
            post.send = request.user
            post.receive = CustomUser.objects.get(pk=Customuser_id)
            post.save()

    context={
        'Contents':TalkContent.objects.filter(
            (Q(receive_id = Customuser_id) &
            Q(send_id = request.user.id)) | (Q(send_id = Customuser_id) &
            Q(receive_id = request.user.id))
        ).order_by("date"),
        'form':forms.TalkForm(),
        'Partner':CustomUser.objects.get(pk=Customuser_id),
        'Self':CustomUser.objects.get(pk=request.user.id)
    }
    return render(request, "myapp/talk_room.html", context)
    

def setting(request):
    return render(request, "myapp/setting.html")

class Signup(CreateView):
    form_class = SignUpForm
    model = CustomUser
    template_name = 'myapp/signup.html'
    success_url = reverse_lazy('index')
#.order_by('date_joined'),

class Logout(LogoutView):
    template_name = 'index.html'

class PasswordChange(PasswordChangeView):
    template_name = 'myapp/passwordchange.html'
    success_url = reverse_lazy("friends")

class UsernameChange(View):
    def get(self, request, *args, **kwargs):
        context = {}
        form = UsernameChangeForm()
        context["form"] = form
        return render(request, 'myapp/usernamechange.html', context)

    def post(self, request, *args, **kwargs):
        form = UsernameChangeForm(request.POST)
        context={}

        if form.is_valid():
            username = form.cleaned_data
            user_obj = CustomUser.objects.get(username =request.user.username)
            user_obj.username = username["username"]
            user_obj.save()

            return redirect("friends")
        else:
            context["form"] = form
            return redirect("setting")

class AdressChange(View):
    def get(self, request, *args, **kwargs):
        context = {}
        form = EmailChangeForm()
        context["form"] = form
        return render(request, 'myapp/emailchange.html', context)

    def post(self, request, *args, **kwargs):
        form = EmailChangeForm(request.POST)
        context={}

        if form.is_valid():
            email = form.cleaned_data
            user_obj = CustomUser.objects.get(email =request.user.email)
            user_obj.email = email["email"]
            user_obj.save()

            return redirect("friends")
        else:
            context["form"] = form
            return redirect("setting")
#最初にifで分けとく
    
class IconChange(View):
    def get(self, request, *args, **kwargs):
        context = {}
        form = IconChangeForm()
        context["form"] = form
        return render(request, 'myapp/iconchange.html', context)

    def post(self, request, *args, **kwargs):
        form = IconChangeForm(request.POST)
        context={}

        if form.is_valid():
            image = form.cleaned_data
            user_obj = CustomUser.objects.get(image =request.user.email)
            user_obj.email = image["image"]
            user_obj.save()

            return redirect("friends")
        else:
            context["form"] = form
            return redirect("setting")

class InquiryView(generic.FormView):
    template_name = "myapp/inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('friends')

    def form_valid(self, form) :
        form.send_email()
        return super().form_valid(form)