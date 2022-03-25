from django.shortcuts import render
from .forms import SignUpForm, TalkForm, LoginForm
from .forms import UsernameUpdateForm, EmailUpdateForm, IconUpdateForm, PasswordUpdateForm
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from .models import Talk, User
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.utils import timezone
import json

def index(request):
    return render(request, "myapp/index.html")

class SignupView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = "myapp/signup.html"
    success_url = reverse_lazy('index')

class Login(LoginView):
    authentication_form = LoginForm
    template_name = 'myapp/login.html'
    
class Logout(LoginRequiredMixin, LogoutView):
    pass
    
class FriendsView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'myapp/friends.html'
    def get_context_data(self, **kwargs):
        context = super(FriendsView, self).get_context_data(**kwargs)
        word = self.request.GET.get('query')
        talk_list = list()
        user_list = list()
        if word:
            user = User.objects.filter(username__iexact=word)            
        else:
            user = User.objects.exclude(username=self.request.user.username).order_by().reverse()
        for user in user:
            print(user)
            if Talk.objects.filter(Q(f_user=self.request.user, t_user=user)|Q(t_user=self.request.user, f_user=user)).exists():
                talk = Talk.objects.filter(Q(f_user=self.request.user, t_user=user)|Q(t_user=self.request.user, f_user=user)).order_by('pub_date').reverse()[0]
                talk.t_user = user
                talk.t_user.id = talk.t_user.id + self.request.user.id
                talk_list.append(talk)
            else:
                user.id = user.id + self.request.user.id
                user_list.append(user)
        context['talk_list'] = talk_list
        context['user_list'] = user_list
        return context        

class TalkView(LoginRequiredMixin, CreateView):
    model = Talk
    form_class = TalkForm
    template_name = "myapp/talk_room.html"
    success_url = reverse_lazy('talk_room')
    def get_success_url(self):
        return reverse('talk_room',kwargs={'id':self.kwargs['id']})
    def form_valid(self, form):

        id = self.kwargs.get('id') - self.request.user.id
        form.instance.f_user = self.request.user
        form.instance.t_user = User.objects.get(id = id)
        return super(TalkView, self).form_valid(form)
    def get_context_data(self, **kwargs):
        id = self.kwargs.get('id') - self.request.user.id
        print(id)
        context = super(TalkView, self).get_context_data(**kwargs)
        context['talk'] = Talk.objects.filter(Q(f_user=self.request.user, t_user__id=id)|Q(t_user=self.request.user, f_user__id=id))
        context['t_user'] = User.objects.get(id = id)
        context['f_user'] = User.objects.get(id = self.request.user.id)
        context['id'] = self.request.user.id
        context['pub_date'] = timezone.now()


        return context

class UsernameUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'myapp/username_update.html'
    form_class = UsernameUpdateForm
    def get_success_url(self):
        return reverse_lazy('username_update_complete')


class EmailUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'myapp/email_update.html'
    form_class = EmailUpdateForm
    def get_success_url(self):
        return reverse_lazy('email_update_complete')

class IconUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'myapp/icon_update.html'
    form_class = IconUpdateForm
    def get_success_url(self):
        return reverse_lazy('icon_update_complete')

class PasswordUpdateView(LoginRequiredMixin,PasswordChangeView):
    template_name = 'myapp/password_update.html'
    form_class = PasswordUpdateForm
    def get_success_url(self):
        return reverse_lazy('password_update_complete')

def username_update_complete(request):
    return render(request, "myapp/username_update_complete.html")
def email_update_complete(request):
    return render(request, "myapp/email_update_complete.html")
def icon_update_complete(request):
    return render(request, "myapp/icon_update_complete.html")
def password_update_complete(request):
    return render(request, "myapp/password_update_complete.html")

def setting(request):
    user = request.user
    params = {
        'user': user
    }
    return render(request, "myapp/setting.html", params)
    


