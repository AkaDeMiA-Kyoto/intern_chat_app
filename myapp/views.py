import operator

from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from .forms import ImageSettingForm, LoginForm, SignUpForm, TalkForm, PasswordChangeForm, MailSettingForm, UserNameSettingForm
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.decorators import login_required
from django.db.models import Q


from .models import Talk

User = get_user_model()

def index(request):
    return render(request, "myapp/index.html")

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = SignUpForm()
    params = {
        'form': form,
    }
    return render(request, "myapp/signup.html", params)

class Login(LoginView):
    authentication_form = LoginForm
    template_name = "myapp/login.html"

class Logout(LogoutView):
    template_name = "myapp/index.html"

@login_required
def friends(request):
    user = request.user
    # requestの中にuserのattributeが存在し、ログインしている使用者を特定するインスタンスが存在
    friends = User.objects.exclude(id=user.id)

    info = []
    info_have_message = []
    info_have_no_message = []

    for friend in friends:
        latest_message = Talk.objects.filter(
            Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend)
        ).order_by('time').last()

        if latest_message:
            info_have_message.append([friend, latest_message.talk, latest_message.time])
        else:
            info_have_no_message.append([friend, None, None])


    info_have_message = sorted(info_have_message, key=operator.itemgetter(2), reverse=True)
    # info_have_messageの三番目の要素を基準にして、info_have_messageを降順に並べ替える

    info.extend(info_have_message)
    info.extend(info_have_no_message)
    # infoリストにinfo_have_messageリストを追加
    # infoリストにinfo_have_no_messageリストを追加

    content = {
        "info": info,
    }
    return render(request, "myapp/friends.html", content)

@login_required
def talk_room(request, user_id):
    user = request.user
    friend = get_object_or_404(User, id=user_id)
    talk = Talk.objects.filter(
        Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend)).order_by('time')
    form = TalkForm()
    context = {
        "form": form,
        "talk": talk,
        "friend": friend,
    }

    if request.method == "POST":
        new_talk = Talk(talk_from = user, talk_to = friend)
        form = TalkForm(request.POST, instance=new_talk)

        if form.is_valid():
            form.save()
            return redirect("talk_room", user_id)
    else:
            print(form.errors)
    return render(request, "myapp/talk_room.html", context)

@login_required
def setting(request):
    return render(request, "myapp/setting.html")

class PasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    # パスワード変更フォーム
    success_url = reverse_lazy("password_change_done")
    # 処理が成功したときのリダイレクト先
    template_name = "myapp/password_change.html"
    # テンプレート

class PasswordChangeDone(PasswordChangeDoneView):
    pass

@login_required
def user_img_change(request):
    user = request.user
    if request.method == 'GET':
        form = ImageSettingForm(instance=user)
        # instance=userをつけることでuserの情報が入った状態のフォームを参照可能
    elif request.method == 'POST':
        form = ImageSettingForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_img_change_done')
        else:
            print(form.errors)

    context = {
        'form': form
    }
    return render(request, 'myapp/user_img_change.html', context)

@login_required
def user_img_change_done(request):
    return render(request, 'myapp/user_img_change_done.html')

@login_required
def mail_change(request):
    user = request.user
    if request.method == 'GET':
        form = MailSettingForm(instance=user)
    elif request.method == 'POST':
        form = MailSettingForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('mail_change_done')
        else:
            print(form.errors)
    context = {
        "form": form,
    }
    return render(request, 'myapp/mail_change.html', context)

@login_required
def mail_change_done(request):
    return render(request, 'myapp/mail_change_done.html')

@login_required
def username_change(request):
    user = request.user
    if request.method == 'GET':
        form = UserNameSettingForm(instance=user)
    elif request.method == 'POST':
        form = UserNameSettingForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('username_change_done')
        else:
            print(form.errors)
    context = {
        'form': form,
    }
    return render(request, 'myapp/username_change.html', context)

@login_required
def username_change_done(request):
    return render(request, 'myapp/username_change_done.html')



# class A:
#     talk_from = ""
#     talk_to = ""

#     def __init__(self, talk_from, talk_to):
#         self.talk_from = talk_from
#         self.talk_to = talk_to

# def sample():
#     a = A("aa", "bb")
