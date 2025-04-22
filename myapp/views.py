import random
from django.shortcuts import redirect,get_object_or_404, render
from django.contrib import messages
from django.contrib.auth import login, logout
from django.db import models
from django.db.models import Q
from .forms import SingupForm, LoginForm, MessageSend, UsernameUpdate, EmailUpdate, PasswordUpdate, ImgUpdate
from django.contrib.auth.decorators import login_required
from .models import Signup, Message
from django.views import View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.conf import settings
from django.core.mail import send_mail


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    form = SingupForm()
    if request.method == "GET": 
        return render(request, "myapp/signup.html", {'form' : form})
    if request.method == "POST":
        form = SingupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("myapp:index")
    return render(request,"myapp/signup.html", {'form' : form})

def login_view(request):
    form = LoginForm()
    if request.method == "GET":
        return render(request, "myapp/login.html", {'form' : form})
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("myapp:friends")
    return render(request, "myapp/login.html", {'form' : form})


class Login(LoginView):
    """ログインページ

    GETの時は指定されたformを指定したテンプレートに表示
    POSTの時はloginを試みる。→成功すればdettingのLOGIN_REDIRECT_URLで指定されたURLに飛ぶ
    """

    authentication_form = LoginForm
    template_name = "myapp/login.html"

    def form_valid(self, form):
        user = form.get_user()
        code = f"{random.randint(0,9999):04}"

        self.request.session['user_id'] = user.id
        self.request.session['verification_code'] = code

        send_mail(
            subject = "ログイン認証コード",
            message= f"認証コード:{code}",
            from_email=settings.DEFAULT_SEND_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,    
        )
        return redirect('myapp:login-verify')

def login_verify(request):
    
    if request.method == "GET":
        return render(request, 'myapp/login-verify.html')
    
    if request.method == "POST":
        user_id = request.session.get('user_id')
        user = Signup.objects.get(id = user_id)
        verify_code = request.session.get('verification_code')
        input_code = request.POST.get('verify_code')
        if input_code == verify_code:
            del request.session['verification_code']
            del request.session['user_id']
            login(request,user)
            return redirect('myapp:friends')
        else:
            messages.error(request,"認証されませんでした。")
        return render(request, 'myapp/login-verify.html')


@login_required
def friends(request):
    users = Signup.objects.exclude(id=request.user.id)
    for user in users:
        partner = get_object_or_404(Signup, id = user.id)
        latest_message =Message.objects.filter(
                Q(recipient = user, sender = request.user)|Q(recipient = request.user, sender = user)
                ).order_by('-sended_at').first()
        partner.latest_message = latest_message
        partner.save()
    users = Signup.objects.exclude(id=request.user.id).order_by(
        models.F('latest_message__sended_at').desc(nulls_last=True), 'id'
        )
    return render(request, "myapp/friends.html", {'users': users})

@login_required
def talk_room(request,user_id):
    form = MessageSend()
    #ユーザー間でトークルームが重複しないための処理
    myself_id = request.user.id
    myself = request.user
    user = get_object_or_404(Signup, id = user_id) #送信相手
    if request.method == "GET":
        #メッセージを送信順に表示する
        messages = Message.objects.filter(Q(sender = myself_id,recipient = user_id)|Q(sender=user_id,recipient=myself_id)).order_by('-sended_at')
        return render(request, "myapp/talk_room.html", {'user':user, 'messages':messages, 'form':form})

    if request.method == "POST":
        form = MessageSend(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = user
            message.save()
            return redirect("myapp:talk_room", user_id = user_id)
        

@login_required
def setting(request):
    return render(request, "myapp/setting.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("myapp:index")

@login_required
def username_update(request):
    form = UsernameUpdate()
    if request.method == "GET":
        login_user = request.user
        return render(request, "myapp/username_update.html", {'form':form, 'user':login_user})
    if request.method == "POST":
        obj = get_object_or_404(Signup, id=request.user.id)
        form = UsernameUpdate(request.POST, instance=obj, request = request)
        if form.is_valid():
            form.save()
            messages.success(request, "ユーザー名を変更しました")
            return redirect("myapp:username_update")
    return render(request, "myapp/username_update.html", {'fomr':form})

@login_required
def email_update(request):
    form = EmailUpdate()
    if request.method == "GET":
        login_user = request.user
        return render(request, "myapp/email_update.html", {'form':form, 'user':login_user})
    if request.method == "POST":
        obj = get_object_or_404(Signup, id=request.user.id)
        form = EmailUpdate(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "メールアドレスを変更しました")
            return redirect("myapp:email_update")
    return render(request, "myapp/email_update.html", {'fomr':form})

@login_required
def password_update(request):
    form = PasswordUpdate()
    if request.method == "GET":
        login_user = request.user
        return render(request, "myapp/password_update.html", {'form':form, 'user':login_user})
    if request.method == "POST":
        obj = get_object_or_404(Signup, id=request.user.id)
        form = PasswordUpdate(request.POST, instance=obj, user = request)
        if form.is_valid():
            form.save()
            messages.success(request, "パスワードを変更しました")
            return redirect("myapp:password_update")
    return render(request, "myapp/password_update.html", {'form':form})

@login_required
def img_update(request):
    form = ImgUpdate()
    if request.method == "GET":
        login_user = request.user
        return render(request, "myapp/img_update.html", {'form':form, 'user':login_user})
    if request.method == "POST":
        obj = get_object_or_404(Signup, id=request.user.id)
        form = ImgUpdate(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "アイコンを変更しました")
            return redirect("myapp:img_update")
    return render(request, "myapp/img_update.html", {'fomr':form})