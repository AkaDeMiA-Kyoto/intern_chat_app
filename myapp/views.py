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
from django.db.models import Q,OuterRef,Subquery,F
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.core.mail import send_mail
import random
from django.contrib import messages
from django.contrib.auth import login

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

    def post(self, request, *args, **kwargs):
        session = request.session

        if "otp_phase" in session:
            user_id = session.get("pre_auth_user_id")
            input_otp = request.POST.get("otp")
            stored_otp = session.get("otp")

            if str(input_otp) == str(stored_otp):
                user = CustomUser.objects.get(id=user_id)
                login(request, user)
                session.pop("otp_phase")
                session.pop("pre_auth_user_id")
                session.pop("otp")
                return redirect('friends')
            else:
                messages.error(request, "OTPが間違っています。")
                return self.form_invalid(self.get_form())
        else:
            form = self.get_form()
            if form.is_valid():
                user = form.get_user()
                otp = random.randint(100000, 999999)
                session["otp"] = otp
                session["otp_phase"] = True
                session["pre_auth_user_id"] = user.id

                send_mail(
                    subject="ログイン用OTP",
                    message=f"あなたのログインコードは {otp} です。",
                    from_email=None,
                    recipient_list=[user.email],
                )
                messages.info(
                    request, "メールに送信された6桁コードを入力してください。"
                )
                return self.form_invalid(form)
            else:
                return self.form_invalid(form)
class LogoutFormView(LoginRequiredMixin,LogoutView):
    template_name = 'myapp/index.html'


@login_required
def friends(request):
    
    user = request.user
    query = request.GET.get('query')
    print(query)
    if query:
        friends = CustomUser.objects.filter( Q(username__icontains=query)|Q(email__icontains=query) ).exclude(id=user.id)
    else:
        friends = CustomUser.objects.all().exclude(id=user.id)

    q_filter = Q(talk_from=user,talk_to=OuterRef("pk"))|Q(talk_to=user,talk_from=OuterRef("pk"))
    ordered_talks = Talk.objects.filter(q_filter).order_by(F('talk_time').desc(nulls_last=True)).reverse()
    friends=(
            CustomUser.objects.exclude(id=user.id)
            .annotate(
                latest_talk = Subquery(ordered_talks.values("talk")[:1])
            )
        )
    context = {
        'friends':friends,
        'user':user,
    }
    return render(request,'myapp/friends.html',context)

@login_required
def talk_room(request ,user_id):
    user = request.user
    friend = get_object_or_404 (CustomUser,id=user_id)
    talks = Talk.objects.select_related("talk_to").select_related("talk_from").filter(
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