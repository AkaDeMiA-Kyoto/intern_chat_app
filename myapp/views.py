from django.shortcuts import redirect, render
from django.contrib import admin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,ListView,CreateView,FormView
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView 
from django.contrib.auth import authenticate
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Message
from .forms import UsernameChangeForm,UserEmailChangeForm,UserImageChangeForm,UserPasswordChangeForm
from .forms import MessageForm
from django.urls import reverse_lazy

Profile = get_user_model()

class Index(TemplateView):
    template_name = "myapp/index.html"
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['goto_signup'] = 'account_signup'
        context['goto_login'] = 'account_login'
        return context


class FriendList(ListView,LoginRequiredMixin):
    template_name = 'myapp/profile_list.html'
    model = Message
        
    def get_context_data(self, **kwargs):
        friends=[]
        never_talked_friends=[]
        user=self.request.user
        #ユーザー以外の友達
        data = Profile.objects.exclude(id=user.id)
        q_word = self.request.GET.get('query')
        if q_word:
            data = Profile.objects.filter(
                Q(username__icontains=q_word))
        else:
            data = Profile.objects.exclude(id=user.id)
        for friend in data:
            latests = Message.objects.all().filter(Q(sender=user) | Q(receiver=user)).filter(Q(sender=friend) | Q(receiver=friend)).order_by('created_at').last()
            if latests != None:
                friends.append([friend,latests])
            else:
                never_talked_friends.append(friend)
        context = super().get_context_data(**kwargs)
        context['friends'] = friends
        context['never_talked_friends'] = never_talked_friends
        return context

class TalkCreate(CreateView,LoginRequiredMixin):
    template_name = 'myapp/talk_room.html'
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse_lazy('myapp:detail',kwargs={'pk':self.kwargs['pk']})

    def form_valid(self,form):
        form.instance.receiver = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.sender = self.request.user
        return super().form_valid(form)
    
    def form_invalid(self,form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = Message.objects.all().reverse()
        context['user'] = self.request.user
        context['receiver'] = Profile.objects.get(pk=self.kwargs['pk'])
        return context

class SettingView(TemplateView,LoginRequiredMixin):
    template_name = 'myapp/setting.html'


class UsernameUpdateView(FormView,LoginRequiredMixin):
    template_name = 'myapp/update_username.html'
    form_class = UsernameChangeForm
    success_url = reverse_lazy('myapp:update_username_complete')

    def form_valid(self, form):
        new_username=form.cleaned_data['username']
        old_obj=Profile.objects.get(username=self.request.user.username)
        print(old_obj.username)
        old_obj.username=new_username
        old_obj.save()
        print(new_username)
        return super().form_valid(form)

    def form_invalid(self,form):
        return super().form_invalid(form)


class UsernameUpdateDoneView(TemplateView,LoginRequiredMixin):
    template_name = 'myapp/update_username_complete.html'

class UserEmailUpdateView(FormView,LoginRequiredMixin):
    template_name = 'myapp/update_email.html'
    form_class = UserEmailChangeForm
    success_url = reverse_lazy('myapp:update_email_complete')

    def form_valid(self, form):
        new_email=form.cleaned_data['email']
        old_obj=Profile.objects.get(email=self.request.user.email)
        print(old_obj.email)
        old_obj.email=new_email
        old_obj.save()
        print(new_email)
        return super().form_valid(form)

    def form_invalid(self,form):
        return super().form_invalid(form)


class UserEmailUpdateDoneView(TemplateView,LoginRequiredMixin):
    template_name = 'myapp/update_email_complete.html'


class UserImageUpdateView(FormView,LoginRequiredMixin):
    template_name = 'myapp/update_image.html'
    form_class = UserImageChangeForm
    success_url = reverse_lazy('myapp:update_image_complete')

    def form_valid(self, form):
        new_image=self.request.FILES['image']
        old_obj=Profile.objects.get(image=self.request.user.image)
        print(old_obj.image)
        old_obj.image=new_image
        old_obj.save()
        print(new_image)
        return super().form_valid(form)

    def form_invalid(self,form):
        return super().form_invalid(form)

class UserImageUpdateDoneView(TemplateView,LoginRequiredMixin):
    template_name = 'myapp/update_image_complete.html'


class PasswordChange(LoginRequiredMixin,PasswordChangeView):
    success_url = reverse_lazy('myapp:update_password_complete')
    template_name = 'myapp/update_password.html'
    form_class = UserPasswordChangeForm

class PasswordChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
    template_name = 'myapp/update_password_complete.html'

