from django.shortcuts import redirect, render, get_object_or_404
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models 
from .models import Message

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = SignUpForm()

    return render(request, 'myapp/signup.html', {'form': form})

# def login_view(request):
#     return render(request, "myapp/login.html")

class login_view(LoginView):
    # ログイン画面のテンプレートを指定
    template_name = 'myapp/login.html'

    # ログイン成功後のリダイレクト先URL名を指定
    authentication_form = AuthenticationForm

# def friends(request):
#     return render(request, "myapp/friends.html")

class friends(LoginRequiredMixin, ListView):
    template_name = 'myapp/friends.html'
    model = get_user_model()
    context_object_name = 'users'

    def get_queryset(self):
        current_user = self.request.user
        all_users = get_user_model().objects.exclude(pk=current_user.pk).exclude(is_staff=True)
        
        user_list = []
        talked_with = set()

        # 1. トークしたことのあるユーザーをリストアップ
        for user in all_users:
            latest_message = Message.objects.filter(
                (models.Q(sender=current_user, receiver=user) | models.Q(sender=user, receiver=current_user))
            ).order_by('-timestamp').first()

            if latest_message:
                user_list.append({
                    'user': user,
                    'latest_talk': latest_message.content,
                    'latest_talk_time': latest_message.timestamp,
                    'has_talked': True,
                })
                talked_with.add(user.pk)

        # 2. まだトークしていないユーザーをリストアップ
        untalked_users = all_users.exclude(pk__in=talked_with).order_by('-date_joined')
        for user in untalked_users:
            user_list.append({
                'user': user,
                'latest_talk': 'まだトークしていません',
                'latest_talk_time': user.date_joined,
                'has_talked': False,
            })

        # 3. トークしたことのあるユーザーを最新トーク時間でソート
        talked_users = sorted([u for u in user_list if u['has_talked']], key=lambda x: x['latest_talk_time'], reverse=True)
        untalked_users = [u for u in user_list if not u['has_talked']]

        return talked_users + untalked_users

class talk_room(LoginRequiredMixin, View):
    def get(self, request, username):
        # URLから渡されたusernameで相手ユーザーを取得
        talk_partner = get_object_or_404(get_user_model(), username=username)
        
        # ここにトーク履歴を取得するロジックを実装
        context = {
            'talk_partner': talk_partner,
            # 'messages': ...
        }
        return render(request, 'myapp/talk_room.html', context)

# def talk_room(request):
#     return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
