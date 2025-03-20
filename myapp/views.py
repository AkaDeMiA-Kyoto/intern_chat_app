from django.shortcuts import redirect, render
from .forms import SignUpForm, LoginForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView

from .models import CustomUser, Talk
from django.db import models
from django.db.models import Q, Subquery, OuterRef
from django.shortcuts import get_object_or_404, redirect

from django.views.generic import TemplateView, CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

#from django.contrib.auth import authenticate #Djangoの認証システム]
#from django.contrib.auth.decorators import login_required



class IndexView(TemplateView):
    template_name = "myapp/index.html"
#def index(request): #requestはウェブサーバー⇀wsgiの流れで送られてきたrequestオブジェクト
    #return render(request, "myapp/index.html")

class SignupView(CreateView):
    model = CustomUser
    form_class = SignUpForm
    template_name = "myapp/signup.html"
    success_url = reverse_lazy("index")

class ChatLoginView(LoginView):
    template_name = "myapp/login.html"
    form_class = LoginForm

class FriendsView(LoginRequiredMixin, ListView):
    model =CustomUser
    template_name = "myapp/friends.html"
    #context_object_name = 'friends'
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user

        # 自分がやり取りした相手を取得
        friends = CustomUser.objects.exclude(pk=user.pk)

        # 最新のトークを取得するサブクエリ
        latest_talks = Talk.objects.filter(
            (Q(send_user=user) & Q(recieve_user=OuterRef('pk'))) |
            (Q(send_user=OuterRef('pk')) & Q(recieve_user=user))
        ).order_by('-talk_at')  # 最新のトーク順

        # friends クエリセットに最新のトーク内容と時刻を追加
        friends = friends.annotate(
            latest_talk=Subquery(latest_talks.values('content')[:1]),  # 最新のメッセージ内容
            latest_talk_time=Subquery(latest_talks.values('talk_at')[:1])  # 最新のメッセージ時刻
        )

        friends = friends.order_by('-latest_talk_time')

        return friends

class TalkroomView(LoginRequiredMixin, TemplateView):
    template_name = 'myapp/talk_room.html'

    def get_context_data(self, **kwargs):
        # 話す相手を取得
        target_user = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        
        # AからB / BからAの両方のトークを取得 (なくてもエラーにならない)
        talks = Talk.objects.filter(
            Q(send_user=self.request.user, recieve_user=target_user) |
            Q(send_user=target_user, recieve_user=self.request.user)
        ).order_by('talk_at')

        # コンテキストデータを返す
        context = super().get_context_data(**kwargs)
        context['friend'] = target_user
        context['talks'] = talks
        return context

    def post(self, request, *args, **kwargs):
        # 話す相手を取得
        target_user = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        content = request.POST.get('content')

        # メッセージをデータベースに保存
        Talk.objects.create(
            send_user=self.request.user,
            recieve_user=target_user,
            content=content
        )

        # トークルームへリダイレクト
        return redirect('talk_room', pk=target_user.pk)

class Setting(LoginRequiredMixin, TemplateView):
    template_name = 'myapp/setting.html'

#ユーザー名変更するやつ
class UsernameChangeView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ["username"]
    template_name = 'myapp/username_change.html'
    success_url = reverse_lazy('setting')

    def get_object(self):
        return self.request.user #現在ログインしているユーザーの取得

#e-mail変更するやつ
class EmailChangeView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ["email"]
    template_name = 'myapp/email_change.html'
    success_url = reverse_lazy('setting')

    def get_object(self):
        return  self.request.user
    
#アイコン変更するやつ
class ImageChangeView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields =["image"]
    template_name = 'myapp/image_change.html'
    success_url = reverse_lazy('setting')

    def get_object(self):
        return self.request.user  


#パスワード変更するやつ
class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('password_change_done')
    template_name = 'myapp/password_change.html'
    login_url = reverse_lazy('index')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "password_change"
        return context
    
class PasswordChangeDone(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'myapp/password_change_done.html'