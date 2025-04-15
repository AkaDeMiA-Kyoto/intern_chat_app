from django.shortcuts import render,redirect,get_object_or_404
from .models import CustomUser,Talk
from .forms import TalkForm
from .forms import SignUpForm
from .forms import UsernameChangeForm
from .forms import MailChangeForm
from .forms import ImageChangeForm
from .forms import LoginForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.core.mail import send_mail
import  datetime

def base(request):
    return render(request, "myapp/base.html")
def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    return render(request, "myapp/signup.html")
    
def login_view(request):
    return render(request, "myapp/login.html")


@login_required
def talk_room(request):
    return render(request, "myapp/talk_room.html")

@login_required
def setting(request):
    return render(request, "myapp/setting.html")

def form_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = SignUpForm()

    return render(request, 'myapp/signup.html', {'form': form})

def send_email(request):
    send_mail(
        '件名',  # 件名
        'メールの本文',  # メッセージ
        'okuru@gmail.com',  # 送信元のメールアドレス
        ['uketoru@gmail.com'],  # 送信先のメールアドレスのリスト
        fail_silently=False,
    )
    return redirect('index') 

class LoginFormView(LoginView):
    authentication_form = LoginForm
    template_name = "myapp/login.html"


class LogoutFormView(LoginRequiredMixin,LogoutView):
    template_name = 'myapp/index.html'

class FriendsListView(LoginRequiredMixin,ListView):
    template_name = 'myapp/friends.html'
    model = CustomUser

def friends(request):
    
    user = request.user
    query = request.GET.get('query')
    if query:
        friends = CustomUser.objects.filter( Q(username__icontains="query")|Q(email__icontains="query") )
    else:
        friends = CustomUser.objects.all()
        
    latest_talks = {}
    for friend in friends:
        q_filter = Q(talk_from=user,talk_to=friend)|Q(talk_to=user,talk_from=friend)
        ordered_talks = Talk.objects.filter(q_filter).order_by('-talk_time')
        if ordered_talks.exists():
            latest_talk = ordered_talks.first()
        else:
            latest_talk = None
        latest_talks[friend.id] = latest_talk
    
    talk_rooms = []

    for friend in friends:
        talk_rooms.append({"time":latest_talks[friend.id].talk_time if latest_talks[friend.id] else None,"value":(friend, latest_talks[friend.id])})
        talk_rooms = sorted(talk_rooms,key = lambda x: (x["time"] is not None,x["time"]),reverse=True)
    context = {
        'friends':friends,
        'user':user,
        'latest_talks': latest_talks,
        'talk_rooms': [talk_room["value"] for talk_room in talk_rooms]
    }
    return render(request,'myapp/friends.html',context)

"""
def friends(request):
    user = request.user
    friends = CustomUser.objects.all()
    latest_talks = {}
    for friend in friends:
        q_filter = Q(talk_from=user,talk_to=friend)|Q(talk_to=user,talk_from=friend)
        ordered_talks = Talk.objects.filter(q_filter).order_by('-talk_time')
        if ordered_talks.exists():
          latest_talk = ordered_talks.first()
        else:
          latest_talk = None
        latest_talks[friend.id] = latest_talk
    
    talk_rooms = []

    for friend in friends:
        talk_rooms.append({"time":latest_talks[friend.id].talk_time if latest_talks[friend.id] else None,"value":(friend, latest_talks[friend.id])})
    talk_rooms = sorted(talk_rooms,key = lambda x: (x["time"] is not None,x["time"]),reverse=True)
    print(talk_rooms)
    # print(latest_talk[id])
    context = {
        'friends':friends,
        'user':user,
        'latest_talks': latest_talks,
        'talk_rooms': [talk_room["value"] for talk_room in talk_rooms]
    }
    return render(request,'myapp/friends.html',context)
"""

@login_required
def talk_room(request ,user_id):
    user = request.user
    friend = get_object_or_404 (CustomUser,id=user_id)
    talks = Talk.objects.filter(
        Q(talk_from=user,talk_to=friend)|Q(talk_to=user,talk_from=friend)
    ).order_by('talk_time')
    form = TalkForm()
    context = {
        'form': form,
        'talks': talks,
        'friend':friend,
        'user':user,
    }
    if request.method == 'POST':
        new_talk = Talk(talk_from=user,talk_to=friend)
        form = TalkForm(request.POST,instance=new_talk)
        if form.is_valid():
            form.save()
            return redirect('talk_room',user_id)
    else:
        return render(request,'myapp/talk_room.html',context)

@login_required
def form_namechange(request):
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UsernameChangeForm()

    return render(request, 'myapp/namechange.html', {'form': form})

@login_required
def form_mailchange(request):
    if request.method == 'POST':
        form = MailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = MailChangeForm()

    return render(request, 'myapp/mailchange.html', {'form': form})

@login_required
def form_imagechange(request):
    if request.method == 'POST':
        form = ImageChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ImageChangeForm()

    return render(request, 'myapp/imagechange.html', {'form': form})

class PasswordChange(LoginRequiredMixin,PasswordChangeView):
    template_name = 'myapp/passwordchange.html'
    success_url = reverse_lazy("index")