from typing import Any, Dict
from urllib import request
from django.forms.models import BaseModelForm
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from urllib import request
from .forms import CustomUserForm,loginform,TalkForm
from django.contrib.auth.views import LoginView
from django.views import generic
from .models import CustomUser
from django.views.generic import ListView,UpdateView, TemplateView
from django.views.generic import DetailView
from .models import Talk
from django.db.models import Q
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.forms import PasswordChangeForm
def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == 'POST':
        form_signup= CustomUserForm(request.POST,request.FILES)

        if form_signup.is_valid():
            form_signup.save()
            params = {"form_signup": form_signup}
            return render(request, "myapp/index.html",{"form_signup": form_signup})
    else:
        form_signup= CustomUserForm()
        params = {"form_signup": form_signup}
    return render(request, "myapp/signup.html",params)

class CustomLoginView(LoginView):
    form_class = loginform
    template_name = "myapp/login.html"
    
    

#def friends(request):
    #return render(request, "myapp/friends.html")

class friendslist(LoginRequiredMixin,generic.ListView):
    model = CustomUser
    template_name = "myapp/friends.html"
    
    def get_context_data(self):
        context = super().get_context_data()
        friends = CustomUser.objects.all().order_by('date_joined')
        context["friends"] = friends # フレンドのid
        my_id = self.request.user.id
        context["my_id"]=my_id
        talks = Talk.objects.all().order_by('time')
        context["talks"]=talks
        return context
    
class TalkRoom(LoginRequiredMixin,generic.FormView):
    model = Talk
    template_name = "myapp/talk_room.html"
    form_class = TalkForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        friend_id = self.kwargs.get("pk") # フレンドのid
        my_id = self.request.user
        context["my_id"]=my_id
        context["friend_id"]=friend_id
        talks = Talk.objects.filter(Q(from_name = friend_id,to_name = my_id)|Q(from_name = my_id,to_name = friend_id)).order_by('time')
        context["talks"] = talks
        friendusername = CustomUser.objects.filter(pk=friend_id).first().username
        context["friendusername"] = friendusername
        return context
    
    def form_valid(self, form):
        data = form.cleaned_data
        from_name = self.request.user
        to_name = CustomUser.objects.get(pk=self.kwargs.get("pk"))
        Talk.objects.create(from_name = from_name,to_name = to_name, contents=data.get("contents"))
        return super().form_valid(form)
    
    def get_success_url(self):
     return reverse_lazy("talk_room",kwargs={"pk":self.kwargs["pk"]} )
 
    # def talk_view(request):
    #     if request.method == 'POST':
    #         form_talklist = TalkForm(request.POST,request.FILES)
            
    #         if form_talklist.is_valid():
    #             form_talklist.save()
    #             params = {"form_talklist": form_talklist}
    #             return render(request, "myapp/talk_room.html", params)
    #     else:
    #         form_talklist= TalkForm()
    #         params = {"form_talklist": form_talklist}
    #     return render(request, "myapp/talk_room.html", params)

class Logout(LoginRequiredMixin,auth_views.LogoutView):
    template_name="myapp/logout.html"
    
    
# def talk_room(request):
#     return render(request, "myapp/talk_room.html")

class Setting(LoginRequiredMixin, generic.TemplateView):
    template_name = 'myapp/setting.html'
    
    def get_context_data(self):
        context = super().get_context_data()
        user_id = self.request.user.id
        context["user_id"]=user_id
        user = self.request.user
        context["user"]=user
        return context
    
    
class UserView(LoginRequiredMixin,generic.UpdateView):
    model = CustomUser
    template_name = 'myapp/user.html'
    success_url = reverse_lazy('finish_view')
    fields=('username',)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id=self.request.user.id
        context["user_id"]=user_id
        return context
    
class EmailView(LoginRequiredMixin,generic.UpdateView):
    model = CustomUser
    template_name = 'myapp/email.html'
    success_url = reverse_lazy('finish_view')
    fields=('email',)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id=self.request.user.id
        context["user_id"]=user_id
        return context
    
    
class IconView(LoginRequiredMixin,generic.UpdateView):
    model = CustomUser
    template_name = 'myapp/icon.html'
    success_url = reverse_lazy('finish_view')
    fields=('img',)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id=self.request.user.id
        context["user_id"]=user_id
        return context

class PasswordChange(LoginRequiredMixin,PasswordChangeView):
    template_name='myapp/password_change.html'
    form_class = PasswordChangeForm
    success_url=reverse_lazy('finish_view')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id=self.request.user.id
        context["user_id"]=user_id
        return context
    
class passwordchangedone(LoginRequiredMixin,PasswordChangeDoneView):
    template_name='myapp/password_change_done.html'
    
def finish_view(request):
    return render(request, "myapp/finish.html")