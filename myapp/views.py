from email.policy import default
from pickle import TRUE
from time import timezone
from tokenize import blank_re
from unittest import load_tests
from unittest.mock import DEFAULT
from django.shortcuts import redirect, render 
from django.urls import reverse_lazy
from django.views import View , generic
from django.views.generic.edit import CreateView
from django import forms
from requests import request
from . import forms 
from myapp.models import CustomUser, TalkContent
from .forms import LoginForm, SignUpForm, UsernameChangeForm ,EmailChangeForm,IconChangeForm
# InquiryForm
from django.contrib.auth.views import LoginView ,LogoutView ,PasswordChangeView
from django.utils import timezone
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import OuterRef, Subquery,F
# from django.views.generic import FormView
# from django.http import HttpResponse , HttpResponseRedirect
# from django.contrib.auth import login
# from datetime import datetime
# from urllib import request


def index(request):
    return render(request, "myapp/index.html")

class Login (LoginView):
    form_class = LoginForm
    template_name = 'myapp/login.html'

# def friends(request):
#     friend_list = CustomUser.objects.all()#exclude(request.user)#excludeで自分消す
#     return render(request, "myapp/friends.html",context={'friend_list':friend_list})

class Friendslist(generic.ListView,LoginRequiredMixin):
    model =CustomUser,TalkContent
    template_name  = 'myapp/friends.html'
    
    def get_queryset(self):
        q_word = self.request.GET.get('query')
        latest_msg = TalkContent.objects.filter(
            Q(send_id=OuterRef("pk"), receive_id=self.request.user)
            | Q(send_id=self.request.user, receive_id=OuterRef("pk"))
            ).order_by("-date")
        if q_word:
            friend_list = (
                    CustomUser.objects.exclude(id=self.request.user.id).filter(
                        Q(username__icontains=q_word)
                        |Q(email__icontains=q_word))
                        ).annotate(latest_msg_talk=Subquery(latest_msg.values("sentence")[:1]),latest_msg_date=Subquery(latest_msg.values("date")[:1],)).order_by(F("latest_msg_date").desc(nulls_last=True),"-date_joined")
            # friend_list = CustomUser.objects.filter(username__icontains=q_word).order_by("-date_joined")
            # talk = TalkContent.objects.filter(
            #     Q(receive_id = self.request.user.id)  & Q(send__in = friend_list) | 
            #     Q(send_id = self.request.user.id) & Q(receive__in = friend_list)
            # ).latest("date")
            # friendtalk = friend_list.union(talk)

        else:
            friend_list = (
                    CustomUser.objects.exclude(id=self.request.user.id).
                    annotate(latest_msg_talk=Subquery(latest_msg.values("sentence")[:1]),latest_msg_date=Subquery(latest_msg.values("date")[:1]))).order_by(F("latest_msg_date").desc(nulls_last=True),"-date_joined")
            # friendtalk = friend_list.union(talk)
        # for i in friend_list:
        #     friend_lists = friend_list + TalkContent.objects.filter(
        #         Q(receive_id = self.request.user.id)  & Q(send = friend_list) | 
        #         Q(send_id = self.request.user.id) & Q(receive = friend_list)).latest("date")
        # friend_lists
        # print(friendtalk)
        return friend_list

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['talk'] = TalkContent.objects.filter(
    #         Q(receive_id = self.request.user)  | 
    #         Q(send_id = self.request.user) ).all
    #     return context

    

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


class Logout(LogoutView):
    template_name = 'index.html'

class PasswordChange(PasswordChangeView):
    template_name = 'myapp/passwordchange.html'
    success_url = reverse_lazy("myapp:friends")

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

# class InquiryView(generic.FormView):
#     template_name = "myapp/inquiry.html"
#     form_class = InquiryForm
#     success_url = reverse_lazy('friends')

#     def form_valid(self, form) :
#         form.send_email()
#         return super().form_valid(form)