from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import (
    TemplateView,
    ListView,
)
from django.utils.decorators import method_decorator
from django.db.models import Subquery, OuterRef, Q
from django.urls import reverse_lazy
from .models import Talk
from .forms import (
    MyLoginForm, TalkForm,
    ChangeUsernameForm, ChangeEmailForm,
    ChangeIconForm, ChangePasswordForm,
)


User = get_user_model()


class IndexView(TemplateView):
    template_name = "myapp/index.html"


class FriendListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'myapp/friends.html'

    def get_queryset(self):
        q_word = self.request.GET.get('query')
        searchtype = self.request.GET.get('search-type')

        if not q_word:
            q_word = ''
        if not searchtype:
            searchtype = 'partial'

        user = self.request.user
        latest_talks = Talk.objects.filter(
            Q(from_user=user, to_user=OuterRef('pk'))
            | Q(from_user=OuterRef('pk'), to_user=user),
        ).order_by('-sent_time')

        if searchtype == 'partial':
            friend_list = User.objects.exclude(id=user.id).filter(username__icontains=q_word).annotate(
                latest_msg=Subquery(latest_talks.values('message')[:1]),
                latest_sent_time=Subquery(latest_talks.values('sent_time')[:1]),
            ).order_by('latest_sent_time', '-date_joined')
        elif searchtype == 'exact':
            friend_list = User.objects.exclude(id=user.id).filter(username__iexact=q_word).annotate(
                latest_msg=Subquery(latest_talks.values('message')[:1]),
                latest_sent_time=Subquery(latest_talks.values('sent_time')[:1]),
            ).order_by('latest_sent_time', '-date_joined')
        else:
            friend_list = User.objects.exclude(id=user.id).exclude(username__icontains=q_word).annotate(
                latest_msg=Subquery(latest_talks.values('message')[:1]),
                latest_sent_time=Subquery(latest_talks.values('sent_time')[:1]),
            ).order_by('latest_sent_time', '-date_joined')

        return friend_list


class TalkRoomView(LoginRequiredMixin, View):
    model = Talk
    template_name = 'myapp/talk_room.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        me = request.user
        friend = User.objects.get(id=pk)

        message_list = Talk.objects.filter(
            Q(from_user=me, to_user=friend)
            | Q(from_user=friend, to_user=me)
        ).order_by('sent_time')

        params = {
            'form': TalkForm(),
            'data': message_list,
            'friend_name': friend.username
        }   
        return render(request, self.template_name, params)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        me = request.user
        friend = User.objects.get(id=pk)

        talk = Talk(from_user=me, to_user=friend)
        form = TalkForm(request.POST, instance=talk)
        if form.is_valid():
            form.save()
            return redirect('talk_room', pk)

        message_list = Talk.objects.filter(
            Q(from_user=me, to_user=friend)
            | Q(from_user=friend, to_user=me)
        ).order_by('sent_time')

        params = {
            'form': TalkForm(),
            'data': message_list,
            'friend_name': user2.username
        } 
        return render(request, self.template_name, params)


class SettingView(LoginRequiredMixin, TemplateView):
    template_name = "myapp/setting.html"


class ChangeUsernameView(LoginRequiredMixin, View):
    template_name = 'myapp/change.html'
    
    def post(self, request, *args, **kwargs):
        form = ChangeUsernameForm(request.POST)
        if form.is_valid():
            user = request.user
            user.username = form.cleaned_data['username']
            user.save()
            messages.success(request, 'Username succesfully changed.')
        params = {
            'form': ChangeUsernameForm(),
            'title': 'ユーザーネーム',
            'link': 'change_username',
        }
        return render(request, self.template_name, params)

    def get(self, request, *args, **kwargs):
        params = {
            'form': ChangeUsernameForm(),
            'title': 'ユーザーネーム',
            'link': 'change_username',
        }
        return render(request, self.template_name, params)


class ChangeEmailView(LoginRequiredMixin, View):
    template_name = 'myapp/change.html'

    def post(self, request, *args, **kwargs):
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            user = request.user
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request, 'Email succesfully changed.')
        params = {
            'form': ChangeEmailForm(),
            'title': 'メールアドレス',
            'link': 'change_email',
        }
        return render(request, self.template_name, params)

    def get(self, request, *args, **kwargs):
        params = {
            'form': ChangeEmailForm(),
            'title': 'メールアドレス',
            'link': 'change_email',
        }
        return render(request, self.template_name, params)


class ChangeIconView(LoginRequiredMixin, View):
    template_name = 'myapp/change.html'

    def post(self, request, *args, **kwargs):
        form = ChangeIconForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            user.img = form.cleaned_data['img']
            user.save()
            messages.success(request, 'Icon Succesfully changed.')
        params= {
            'form': ChangeIconForm(),
            'title': 'アイコン',
            'link': 'change_icon',
        }
        return render(request, self.template_name, params)

    def get(self, request, *args, **kwargs):
        params= {
            'form': ChangeIconForm(),
            'title': 'アイコン',
            'link': 'change_icon',
        }
        return render(request, self.template_name, params)

