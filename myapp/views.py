from django.shortcuts import get_object_or_404, redirect, render
from .forms import SignupForm, LoginForm, UserChangeForm, EmailChangeForm, IconChangeForm
from django.contrib.auth.views import LoginView, LogoutView
from .models import Friend
from .models import Talk
from django.contrib.auth import get_user_model
from django.db.models import Q
from .forms import TalkForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()  # ユーザー情報をデータベースに保存
            return redirect('index')  # 登録後はindexページなどにリダイレクト
    else:
        form = SignupForm()
    return render(request, 'myapp/signup.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             class Login(LoginView):
#                 authentication_form = LoginForm
#                 template_name = "myapp/login.html"
#     else:
#         form = LoginForm()
#     return render(request, "myapp/login.html", {"form": form})

class login_view(LoginView):
    authentication_form = LoginForm
    template_name = "myapp/login.html"

def friends(request):
    friends = Friend.objects.all()
    friend_list = []
    for friend in friends:
        latest_talk = friend.content
        latest_time = friend.created_at
        friend_info = {
            'friend': friend,
            'talk': latest_talk,
            'time': latest_time,
        }
        friend_list.append(friend_info)
    context = {'friends': friend_list}
    return render(request, 'myapp/friends.html', context)

def talk_room(request, friend_id):
    User = get_user_model()
    sender_user = request.user
    recipient_user = User.objects.get(id=friend_id)

    # sender_userからrecipient_userへのトーク一覧を取得
    talks = Talk.objects.filter(
    Q(sender=sender_user, recipient=recipient_user) | 
    Q(sender=recipient_user, recipient=sender_user)
).order_by("created_at")
    talk_list =[]
    for talk in talks:
        talk_info = {
            'sender': talk.sender,
            'recipient': talk.recipient,
            'talk': talk.content,
            'time': talk.created_at,
        }
        talk_list.append(talk_info)

    if request.method == 'POST':
        talk_content = Talk(sender=request.user, recipient=recipient_user)
        form = TalkForm(request.POST, instance=talk_content)
        if form.is_valid():
            form.save()  # データベースに保存
            return redirect('talk_room', friend_id)  # 成功ページへリダイレクト
    else:
        form = TalkForm()
    
    context = {'talks': talk_list,
               'sender': sender_user,
               'recipient': recipient_user,
               'form': form,
               }
    return render(request, "myapp/talk_room.html", context)

# def message(request):
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             form.save()  # データベースに保存
#             return redirect('success')  # 成功ページへリダイレクト
#     else:
#         form = MessageForm()
#     return render(request, 'contact.html', {'form': form})

def setting(request):
    return render(request, "myapp/setting.html")

def setting_username(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('setting_complete')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, "myapp/setting_username.html", {'form': form})

def setting_email(request):
    if request.method == "POST":
        form = EmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('setting_complete')
    else:
        form = EmailChangeForm(instance=request.user)
    return render(request, "myapp/setting_email.html", {'form': form})

def setting_icon(request):
    if request.method == "POST":
        form = IconChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('setting_complete')
    else:
        form = IconChangeForm(instance=request.user)
    return render(request, "myapp/setting_icon.html", {'form': form})

def setting_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # セッションを更新
            return redirect('setting_complete')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'myapp/setting_password.html', {'form': form})

# class setting_password(PasswordChangeView):
#     template_name = "myapp/setting_password.html"

class setting_logout(LogoutView):
    template_name = "myapp/setting_logout.html"
    next_page = 'index'
    http_method_names = ['get', 'post'] 

def setting_complete(request):
    return render(request, "myapp/setting_complete.html")


    # form = MessageForm(request.POST or None)
    # if request.method == "POST":
    #     if form.is_valid():
    #         # メッセージ送信時の保存処理（Talkモデルに紐付ける場合）
    #         Talk.objects.create(
    #             sender=sender_user,
    #             recipient=recipient_user,
    #             content=form.cleaned_data['message']
    #         )
    #         return redirect('talk_room', friend_id=friend_id)
    # else:
    #     form = MessageForm()