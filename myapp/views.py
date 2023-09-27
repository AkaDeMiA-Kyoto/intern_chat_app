from django.shortcuts import redirect, render, get_object_or_404
from .forms import SignUpForm, LogInView, ChangeNameForm, ChangeMailForm, ChangeIconForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .forms import LogInForm, MessageForm
from .models import CustomUser, Message
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, LogoutView

# トップ画面
def index(request):
    return render(request, "myapp/index.html")

# ログイン
class login_view(LoginRequiredMixin, TemplateView):
    template_name = 'myapp/friends.html'
    login_url = 'login'

class login(LogInView):
    template_name = 'myapp/login.html'
    form_class = LogInForm

# ログアウト
class logout(LogoutView):
    template_name='index.html'

# 新規登録
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(to = 'index')
    else:
        form = SignUpForm()

    return render(request, "myapp/signup.html", {"form": form})

# フレンド一覧
def friends(request):
    UserData = CustomUser.objects.exclude(id=request.user.id)
    already_list = []
    yet_list = []
    already_list[:] = []
    yet_list[:] = []
    print(request.user)
    for friend in UserData:
        latests = Message.objects.all().filter(Q(sender=request.user.id)|Q(opposer=request.user.id)).filter(Q(sender=friend.id)|Q(opposer=friend.id)).order_by("-message_date").first()
        if latests != None:
            already_list.append([latests.message_date, friend, latests])
        else:
            yet_list.append([friend.date_joined, friend])
    
    already_list.sort(key=lambda x: x[0], reverse=True)
    yet_list.sort(key=lambda x: x[0], reverse=True)

    params = {
        'already': already_list,
        'yet': yet_list,
    }
    return render(request, "myapp/friends.html", params)

# トーク画面
def talk_room(request, username):
    if request.method == 'POST':
        obj = Message()
        message = MessageForm(request.POST, instance=obj)
        if message.is_valid():
            content = message.cleaned_data['content']
            messages = Message(content=content, opposer=CustomUser.objects.get(id=username), sender=CustomUser.objects.get(id=request.user.id))
            messages.save()
            return redirect("talk_room", username=username)
    
    realname = CustomUser.objects.get(id=username)
    data = Message.objects.all().filter(Q(sender=request.user.id)|Q(opposer=request.user.id)).filter(Q(sender=username)|Q(opposer=username))
    params = {
        'data': data,
        'form': MessageForm(),
        'username': username,
        'realname': realname,
    }
    return render(request, "myapp/talk_room.html", params)

# 設定
def setting(request):
    return render(request, "myapp/setting.html")

# ユーザ名変更
def name(request):
    name = get_object_or_404(CustomUser, pk=request.user.id)
    if request.method == 'POST':
        form = ChangeNameForm(request.POST, instance=name)
        if form.is_valid():
            form.save()
            return redirect(to = 'updatename')
    else:
        form = ChangeNameForm()

    return render(request, "myapp/changename.html", {'form': form})

def updatename(request):
    return render(request, "myapp/updatename.html")

# メールアドレス変更
def mail(request):
    mail = get_object_or_404(CustomUser, pk=request.user.id)
    if request.method == 'POST':
        form = ChangeMailForm(request.POST, instance=mail)
        if form.is_valid():
            form.save()
            return redirect(to = 'updatemail')
    else:
        form = ChangeMailForm()

    return render(request, "myapp/changemail.html", {'form': form})

def updatemail(request):
    return render(request, "myapp/updatemail.html")

# アイコン変更
def icon(request):
    icon = get_object_or_404(CustomUser, pk=request.user.id)
    if request.method == 'POST':
        form = ChangeIconForm(request.POST, request.FILES, instance=icon)
        if form.is_valid():
            form.save()
            return redirect(to = 'updateicon')
    else:
        form = ChangeIconForm()

    return render(request, "myapp/changeicon.html", {'form': form})

def updateicon(request):
    return render(request, "myapp/updateicon.html")

# パスワード変更
class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('updatepassword')
    template_name = 'myapp/changepassword.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "password_change"
        return context
    
class PasswordChangeDone(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'myapp/updatepassword.html'