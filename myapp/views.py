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
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

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

class login_view(LoginView):
    # ログイン画面のテンプレートを指定
    template_name = 'myapp/login.html'

    # ログイン成功後のリダイレクト先URL名を指定
    authentication_form = AuthenticationForm

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

        messages = Message.objects.filter(
            models.Q(sender=request.user, receiver=talk_partner) | models.Q(sender=talk_partner, receiver=request.user)
        ).order_by('timestamp')
        
        # ここにトーク履歴を取得するロジックを実装
        context = {
            'talk_partner': talk_partner,
            'messages': messages,
        }
        return render(request, 'myapp/talk_room.html', context)
    
    def post(self, request, username):
        talk_partner = get_object_or_404(get_user_model(), username=username)
        content = request.POST.get('content')
        
        if content:
            # 新しいメッセージをデータベースに保存
            Message.objects.create(
                sender=request.user,
                receiver=talk_partner,
                content=content
            )
        
        # 同じトークルームにリダイレクトして、画面を更新
        return redirect('talk_room', username=username)

def setting(request):
    return render(request, "myapp/setting.html")

class username(LoginRequiredMixin, View):
    def get(self, request):
        # ユーザー名変更ページを表示
        return render(request, 'myapp/username.html')

    def post(self, request):
        new_username = request.POST.get('new_username')
        user = request.user

        if new_username:
            # 新しいユーザー名がすでに使われているか確認
            if user.__class__.objects.filter(username=new_username).exists():
                messages.error(request, 'このユーザー名はすでに使用されています。')
            else:
                user.username = new_username
                user.save()
                messages.success(request, 'ユーザー名を変更しました。')
                return redirect('username')

        return render(request, 'myapp/username.html')
    
class email(LoginRequiredMixin, View):
    def get(self, request):
        # メールアドレス変更ページを表示
        return render(request, 'myapp/email.html')

    def post(self, request):
        new_email = request.POST.get('new_email')
        user = request.user

        if new_email:
            # 1. メールアドレスの形式を検証
            try:
                validate_email(new_email)
            except ValidationError:
                messages.error(request, '無効なメールアドレスです。')
                return render(request, 'myapp/email.html')
                
            user.email = new_email
            user.save()
            messages.success(request, 'メールアドレスを変更しました。')
            return redirect('change_email')

        return render(request, 'myapp/email.html')
    
class icon(LoginRequiredMixin, View):
    def get(self, request):
        # アイコン変更ページを表示
        return render(request, 'myapp/icon.html')

    def post(self, request):
        new_icon = request.FILES.get('new_icon')
        user = request.user

        if new_icon:
            # 既存のアイコンを削除
            if user.image:
                user.image.delete(save=False)
            
            # 新しいアイコンをアップロード
            user.image = new_icon
            user.save()
            
            messages.success(request, 'アイコンを変更しました。')
            return redirect('icon')
        else:
            messages.error(request, 'ファイルが選択されていません。')

        return render(request, 'myapp/icon.html')
