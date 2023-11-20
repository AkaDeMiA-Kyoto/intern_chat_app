from typing import Any, Dict
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.contrib.auth import login, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import SignUpForm, LoginForm, MessageForm, MyPasswordChangeForm, EmailChangeForm, UsernameChangeForm, ImageChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, LogoutView
from .models import CustomUser, Message
from django.db.models import Max, F, ExpressionWrapper, DateTimeField, When, Case, Q, Subquery
from django.db.models.functions import Coalesce
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            if 'image' in request.FILES:
                user.image = request.FILES['image']
                user.save()
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, "myapp/signup.html", {'form': form})

class login_view(LoginView):
    template_name = 'myapp/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        # ユーザーを認証
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # ユーザーが正しく認証された場合、ログイン
            login(self.request, user)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

@login_required
def friends(request):
    user = request.user
    users = CustomUser.objects.exclude(id=user.id)
    # user = CustomUser.objects.get(username=request.user.username)
    # print(user.id)
    # print(user.pk)

    # # チャットをしたユーザーの最後のメッセージ送信時刻を取得
    # chat_users = CustomUser.objects.exclude(id=user.id).filter(
    #     Q(send_from=user) | Q(send_to=user)
    # ).distinct()

    # chat_users_subquery = Message.objects.filter(
    #     Q(send_from=user, send_to=F('user_id')) | Q(send_to=user, send_from=F('user_id'))
    # ).order_by('user_id', '-send_at').distinct('user_id')

    # chat_users = chat_users.annotate(
    #     last_chat_time=Coalesce(
    #         Subquery(chat_users_subquery.values('send_at')[:1]), F('created_at'), output_field=DateTimeField()
    #     )
    # )

    # # チャットをしていないユーザーの作成日時を取得
    # non_chat_users = CustomUser.objects.exclude(id=user.id).exclude(id__in=chat_users.values('id'))

    # # ユーザーをチャットした有無と時刻に基づいて結合
    # users = chat_users | non_chat_users
    
    return render(request, "myapp/friends.html", {'users': users})

@login_required
def talk_room(request, id):
    user1 = request.user
    user2 = CustomUser.objects.get(id=id)
    messages = Message.objects.filter(
        Q(send_from=user1) & Q(send_to=user2) | Q(send_from=user2) & Q(send_to=user1)
    ).order_by('send_at')
    
    form = MessageForm()
    
    context = {'user1': user1, 'user2': user2, 'messages': messages, 'form': form}
    
    return render(request, "myapp/talk_room.html", context)

@login_required
def send_message(request, id):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            user1 = request.user
            user2 = CustomUser.objects.get(id=id)
            message = Message(send_from=user1, send_to=user2, content=content)
            message.save()
            messages.success(request, 'メッセージが送信されました')
        else:
            messages.error(request, 'メッセージの送信に失敗しました')
    return redirect('talk_room', id=id)

@login_required
def setting(request):
    return render(request, "myapp/setting.html")

class password_change(LoginRequiredMixin, PasswordChangeView):
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('setting_done')
    template_name = 'myapp/password_change.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['process_name'] = 'Change Password'
        return context

class setting_done(LoginRequiredMixin, PasswordChangeDoneView, TemplateView):
    template_name = 'myapp/setting_done.html'

class logout(LoginRequiredMixin, LogoutView):
    template_name = 'myapp/logout.html'

@login_required
def email_change(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            user.email = form.cleaned_data['new_email1']
            user.save()
            return redirect('setting_done')
    else:
        form = EmailChangeForm()
    return render(request, 'myapp/email_change.html', {'form': form})

@login_required
def username_change(request):
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            user.username = form.cleaned_data['new_username1']
            user.save()
            return redirect('setting_done')
    else:
        form = UsernameChangeForm()
    return render(request, 'myapp/username_change.html', {'form': form})

@login_required
def image_change(request):
    if request.method == 'POST':
        print('A')
        form = ImageChangeForm(request.POST, request.FILES)
        if form.is_valid():
            print('B')
            user = request.user
            if 'image' in request.FILES:
                print('C')
                user.image = request.FILES['image']
                user.save()
            return redirect('setting_done')
    else:
        form = ImageChangeForm()
    return render(request, 'myapp/image_change.html', {'form': form})