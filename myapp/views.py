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
                return redirect("friend")
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
'''
    def form_invalid(self, form):
        res = super().form_invalid(form)
        res.status_code = 400
        return res

    def form_valid(self, form):
        otp = random(100000,999999)
        send_mail
        
        try:
            form = LoginForm(self.request.POST)
            rval = super().form_valid(form)
            if rval.status_code >= 300 and rval.status_code < 400:
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password1"]
                backend = CustomUserBackend()
                user = backend.authenticate(
                    self.request, email=email, password=password
                )
                if user is None:
                    return HttpResponseServerError(f"Server Error:{e}")

                self.request.session["is_provisional_signup"] = True
                self.request.session["user_id"] = user.id
                tmp_time = datetime.now(tz=timezone.utc) + timedelta(seconds=300)
                self.request.session["exp"] = str(tmp_time.timestamp())  # 5minutes

                url = TwoFA().app(user)
                data = {"qr": make_qr(url)}
                return render(self.request, "friends.html", data)

            else:
                rval.satus_code = 400
                return rval
        except Exception as e:
            return HttpResponseServerError(f"Server Error:{e}")
'''
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