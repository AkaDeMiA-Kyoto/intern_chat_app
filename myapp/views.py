from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm, TalkForm, UsernameUpdateForm, UseradressUpdateForm, UserimageUpdateForm, CustomPasswordChangeForm
from .models import Message, CustomUser
from django.contrib.auth import login, logout, get_user_model, update_session_auth_hash
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import operator

Custom_User = get_user_model()

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'myapp/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        next_url = request.POST.get('next')
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                if not next_url or next_url == 'None':
                    return redirect('index')
                else:
                    return redirect(next_url)
    else:
        form = CustomAuthenticationForm()
        next_url = request.GET.get('next')
    return render(request, 'myapp/login.html', {'form': form, 'next': next_url})

@login_required
def friends(request):
    friends = CustomUser.objects.exclude(id=request.user.id)
    
    info = []
    info_have_message = []
    info_have_no_message = []
    
    for friend in friends:
        last_message = Message.objects.filter(
                Q(sender=request.user, recipient=friend) | Q(sender=friend, recipient=request.user)
        ).order_by('timestamp').last()
        
        if last_message:
            info_have_message.append([friend, last_message.content, last_message.timestamp])
        else:
            info_have_no_message.append([friend, None, None])
    
    info_have_message = sorted(info_have_message, key=operator.itemgetter(2), reverse=True)
    
    info.extend(info_have_message)
    info.extend(info_have_no_message)
    
    return render(request, "myapp/friends.html", {"info": info})

@login_required
def talk_room(request, user_id):
    friend = get_object_or_404(CustomUser, id=user_id)
    form = TalkForm()

    if request.method == "POST":
        form = TalkForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = friend
            message.save()
            return redirect('talk_room', user_id=user_id)

    talks = Message.objects.filter(
        Q(sender=request.user, recipient=friend) | Q(sender=friend, recipient=request.user)
    ).order_by('timestamp')

    return render(request, "myapp/talk_room.html", {
        'form': form,
        'talks': talks,
        'friend': friend,
    })

@login_required
def setting(request):
    return render(request, "myapp/setting.html", {})

@login_required
def setting_username(request):
    user = request.user

    if request.method == "POST":
        user_form = UsernameUpdateForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "ユーザー名が更新されました。")
            return redirect('setting')

    else:
        user_form = UsernameUpdateForm(instance=user)
    return render(request, "myapp/setting_username.html", {
        'user_form': user_form,
        'current_username': user.username,
        })

@login_required
def setting_adress(request):
    user = request.user

    if request.method == "POST":
        user_form = UseradressUpdateForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "メールアドレスが更新されました。")
            return redirect('setting')
        else:
            print(user_form.errors) 


    else:
        user_form = UseradressUpdateForm(instance=user)

    return render(request, "myapp/setting_adress.html", {
        'user_form': user_form,
        'current_adress': user.email,
        })

@login_required
def setting_image(request):
    user = request.user

    if request.method == "POST":
        user_form = UserimageUpdateForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "プロフィール画像が更新されました。")
            return redirect('setting')

    else:
        user_form = UserimageUpdateForm(instance=user)

    return render(request, "myapp/setting_image.html", {'user_form': user_form})

@login_required
def setting_password(request):
    user = request.user

    if request.method == "POST":
        password_form = CustomPasswordChangeForm(user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "パスワードが変更されました。")
            return redirect('setting')
        else:
            messages.error(request, "パスワード変更に失敗しました。")
    else:
        password_form = CustomPasswordChangeForm(user)

    return render(request, "myapp/setting_password.html", {
        'password_form': password_form,
        })

@login_required
def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect('index')