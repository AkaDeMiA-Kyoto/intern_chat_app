from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm, TalkForm, UsernameUpdateForm, UseradressUpdateForm, UserimageUpdateForm, CustomPasswordChangeForm, UserSearchForm
from .models import Message, CustomUser
from django.contrib.auth import login, logout, get_user_model, update_session_auth_hash, authenticate
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import operator
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib import messages
import random

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

def users_mail_test(request):
    code = random.randint(1000, 9999)
    request.session['auth_code'] = str(code)
    username = request.POST.get('username')
    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        messages.error(request, '指定されたユーザー名は存在しません。')
        return redirect('login_view')

    send_mail(
        '2段階認証',
        f'認証コードは {str(code)} です。',
        settings.EMAIL_FROM,
        [user.email],
        fail_silently=False
    )
    messages.success(request, f'認証コードが {user.email} に送信されました。')
    return redirect('login_with_code')

def login_view(request):
    confirmed_username = request.session.get('confirmed_username', None)

    if request.method == 'POST':
        if 'clear_username' in request.POST:
            request.session.pop('confirmed_username', None)
            messages.info(request, 'ユーザー名を再入力してください。')
            form = CustomAuthenticationForm()
            confirmed_username = None

        elif 'send_code' in request.POST:
            username = request.POST.get('username')

            if not username:
                messages.error(request, 'ユーザー名を入力してください。')
                form = CustomAuthenticationForm()
            else:
                try:
                    user = CustomUser.objects.get(username=username)
                    code = random.randint(1000, 9999)
                    request.session['auth_code'] = str(code)
                    request.session['confirmed_username'] = username

                    send_mail(
                        '2段階認証',
                        f'認証コードは {str(code)} です。',
                        settings.EMAIL_FROM,
                        [user.email],
                        fail_silently=False
                    )
                    messages.success(request, f'認証コードが {user.email} に送信されました。')
                except CustomUser.DoesNotExist:
                    messages.error(request, '指定されたユーザー名は存在しません。')
                form = CustomAuthenticationForm()
                confirmed_username = request.session.get('confirmed_username', None)

        else:
            if confirmed_username:
                request.POST = request.POST.copy()
                request.POST['username'] = confirmed_username

            form = CustomAuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = request.session.get('confirmed_username')
                password = form.cleaned_data.get('password')
                input_code = form.cleaned_data.get('code_form')
                saved_code = request.session.get('auth_code')

                if input_code == saved_code:
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login(request, user)
                        messages.success(request, 'ログインに成功しました。')
                        return redirect('friends')
                    else:
                        messages.error(request, 'パスワードが正しくありません。')
                else:
                    messages.error(request, '認証コードが正しくありません。')
            else:
                messages.error(request, 'フォームの入力に誤りがあります。')

    else:
        form = CustomAuthenticationForm()

    return render(request, 'myapp/login.html', {'form': form, 'confirmed_username': confirmed_username})


@login_required
def friends(request):
    form = UserSearchForm(request.GET)
    friends = CustomUser.objects.exclude(id=request.user.id).prefetch_related('sent_messages', 'received_messages')

    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            friends = friends.filter(
                Q(username__icontains=query) | Q(email__icontains=query)
            )

    info = []
    info_have_message = []
    info_have_no_message = []

    last_messages = Message.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).select_related('sender', 'recipient').order_by('timestamp')

    message_dict = {}
    for message in last_messages:
        if message.sender_id == request.user.id:
            message_dict[message.recipient_id] = message
        else:
            message_dict[message.sender_id] = message

    for friend in friends:
        last_message = message_dict.get(friend.id)
        if last_message:
            info_have_message.append([friend, last_message.content, last_message.timestamp])
        else:
            info_have_no_message.append([friend, None, None])

    info_have_message = sorted(info_have_message, key=operator.itemgetter(2), reverse=True)
    info.extend(info_have_message)
    info.extend(info_have_no_message)

    return render(request, "myapp/friends.html", {"info": info, "form": form})


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
    ).select_related('sender', 'recipient').order_by('timestamp')

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
