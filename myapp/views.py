from django.shortcuts import redirect, render
from django.db.models import Max
from django.db.models.functions import Greatest, Coalesce
from django.contrib import admin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,ListView,View,FormView
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

    def get(self, request, *args, **kwargs):
        friends = []
        never_talked_friends =[]
        user = self.request.user
        friend_data = Profile.objects.exclude(id = user.id)
        q_word = self.request.GET.get('query')
        if q_word:
            friend_data = Profile.objects.filter(
                Q(username__icontains=q_word)
            )
        
        else:
            friend_data = Profile.objects.exclude(id=user.id)

        for friend in friend_data:
            latests = Message.objects.all().filter(Q(sender=user) | Q(receiver=user)).filter(Q(sender=friend) | Q(receiver=friend)).order_by('created_at').last()
            if latests != None:
                friends.append([friend,latests])

            else:
                never_talked_friends.append(friend)

        return render(request,'myapp/profile_list.html',{
            'friends':friends,
            'never_talked_friends':never_talked_friends
        })


class TalkCreate(View,LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        friend = Profile.objects.get(pk=self.kwargs['pk'])
        user = self.request.user
        user_name = user.username
        message_content = Message.objects.all().reverse()
        form = MessageForm(request.POST or None)

        return render(request, 'myapp/talk_room.html',{
            'user_name':user_name,
            'user':user,
            'friend':friend,
            'data':message_content,
            'form':form
        })


class SettingView(TemplateView,LoginRequiredMixin):
    template_name = 'myapp/setting.html'


class UsernameUpdateDoneView(TemplateView,LoginRequiredMixin):
    template_name = 'myapp/update_username_complete.html'



class UsernameUpdateView(View,LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        form = UsernameChangeForm(request.POST or None)

        return render(request, 'myapp/update_username.html', {
            'form':form
        })
    
    def post(self, request, *args, **kwargs):
        form = UsernameChangeForm(request.POST or None)

        if form.is_valid():
            new_username = form.cleaned_data['username']
            old_obj = Profile.objects.get(username = self.request.user.username)
            old_obj.username = new_username
            old_obj.save()
            return redirect('myapp:update_username_complete')

        return render(request, 'myapp/update_username.html', {
            'form':form
        })


class UserEmailUpdateView(View,LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        form = UserEmailChangeForm(request.POST or None)

        return render(request, 'myapp/update_email.html', {
            'form':form
        })
    
    def post(self, request, *args, **kwargs):
        form = UserEmailChangeForm(request.POST or None)

        if form.is_valid():
            new_email = form.cleaned_data['email']
            old_obj = Profile.objects.get(email = self.request.user.email)
            old_obj.email = new_email
            old_obj.save()
            return redirect('myapp:update_email_complete')

        return render(request, 'myapp/update_email.html', {
            'form':form
        })


class UserEmailUpdateDoneView(TemplateView,LoginRequiredMixin):
    template_name = 'myapp/update_email_complete.html'


class UserImageUpdateView(View,LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        form = UserImageChangeForm(request.FILES or None)

        return render(request, 'myapp/update_image.html', {
            'form':form
        })
    
    def post(self, request, *args, **kwargs):
        form = UserImageChangeForm(request.FILES or None)

        if form.is_valid():
            new_image = self.request.FILES['image']
            old_obj = Profile.objects.get(image = self.request.user.image)
            old_obj.image = new_image
            old_obj.save()
            return redirect('myapp:update_image_complete')

        return render(request, 'myapp/update_image.html', {
            'form':form
        })


class UserImageUpdateDoneView(TemplateView,LoginRequiredMixin):
    template_name = 'myapp/update_image_complete.html'


class PasswordChange(LoginRequiredMixin,PasswordChangeView):
    success_url = reverse_lazy('myapp:update_password_complete')
    template_name = 'myapp/update_password.html'
    form_class = UserPasswordChangeForm

class PasswordChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
    template_name = 'myapp/update_password_complete.html'

