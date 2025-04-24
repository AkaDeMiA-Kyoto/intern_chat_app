import operator
import random

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
)
from django.core.mail import send_mail
from django.db.models import OuterRef, Q, Subquery
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from .forms import (
    ImageSettingForm,
    LoginForm,
    MailSettingForm,
    PasswordChangeForm,
    SignUpForm,
    TalkForm,
    UserNameSettingForm,
)
from .models import Talk

User = get_user_model()


def index(request):
    return render(request, "myapp/index.html")


def signup_view(request):
    phase = request.session.get("otp_phase", "form_phase")

    if request.method == "POST" and phase == "form_phase":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            request.session["signup_data"] = {
                "username": form.cleaned_data["username"],
                "email": form.cleaned_data["email"],
                "password1": form.cleaned_data["password1"],}
            otp = random.randint(100000, 999999)
            request.session["otp"] = str(otp)
            request.session["otp_phase"] = "otp_phase"
            
            send_mail(
                subject="登録用OTP",
                message=f"あなたの確認コードは {otp} です。",
                from_email=None,
                recipient_list=[form.cleaned_data["email"]],
            )
        
            messages.info(request, "メールに送られた6桁コードを入力してください。")
            return redirect("signup")
        else:
            print(form.errors)
    elif request.method == "POST" and phase == "otp_phase":
        input_otp = request.POST.get("otp")
        stored_otp = request.session.get("otp")
        
        if str(input_otp) == str(stored_otp):
            data = request.session.get("signup_data")
            user_model = get_user_model()
            user = user_model.objects.create_user(
                username=data["username"],
                password=data["password1"],
                email=data["email"],
                icon=request.FILES.get("icon") if request.FILES.get("icon") else None
            )
            login(request, user)
            request.session.pop("signup_data", None)
            request.session.pop("otp_phase", None)
            request.session.pop("otp", None)
            
            return redirect("friends")
        else:
            messages.error(request, "OTPが間違っています。")
            return redirect("signup")
    
    else:
        form = SignUpForm()

    return render(request, "myapp/signup.html", {
        "form": form,
        "otp_phase": phase
    })

class Login(LoginView):
    """ログインページ

    GETの時は指定されたformを指定したテンプレートに表示
    POSTの時はloginを試みる。→成功すればdettingのLOGIN_REDIRECT_URLで指定されたURLに飛ぶ
    """

    authentication_form = LoginForm
    template_name = "myapp/login.html"
    
    def post(self, request, *args, **kwargs):

        if "otp_phase" in request.session:
            user_id = request.session.get("pre_auth_user_id")
            input_otp = request.POST.get("otp")
            stored_otp = request.session.get("otp")

            if str(input_otp) == str(stored_otp):
                user = User.objects.get(id=user_id)
                login(request, user)
                request.session.pop("otp_phase")
                request.session.pop("pre_auth_user_id")
                request.session.pop("otp")
                return redirect("friends")
            else:
                messages.error(request, "OTPが間違っています。")
                return self.form_invalid(self.get_form())

        else:
            form = self.get_form()
            if form.is_valid():
                user = form.get_user()
                otp = random.randint(100000, 999999)
                request.session["otp"] = otp
                request.session["otp_phase"] = True
                request.session["pre_auth_user_id"] = user.id

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


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""


@login_required
def friends(request):
    user = request.user
    
    latest_message = Talk.objects.filter(
        Q(talk_from=user, talk_to=OuterRef("pk")) | Q(talk_from=OuterRef("pk"), talk_to=user)
    ).order_by("-time")
    
    friends = User.objects.exclude(id=user.id).annotate(
        latest_message_talk=Subquery(latest_message.values("talk")[:1]),
        latest_message_time=Subquery(latest_message.values("time")[:1]),
    )

    
    
    query = request.GET.get('query')

    if query:
        people_list = friends.filter(
                Q(username__icontains=query) | Q(email__icontains=query))
        
    else:
        people_list = friends
        
    info=[
        (friend, friend.latest_message_talk, friend.latest_message_time)
        for friend in people_list
    ]
    
    context = {
        'info': info, 'people_list': people_list, 'query': query
    }
    return render(request, "myapp/friends.html", context)


@login_required
def talk_room(request, user_id):
    # ユーザ・友達をともにオブジェクトで取得
    user = request.user
    friend = get_object_or_404(User, id=user_id)
    # 自分→友達、友達→自分のトークを全て取得
    talk = Talk.objects.filter(
        Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend)
    ).order_by("time")
    # 送信form
    form = TalkForm()
    # メッセージ送信だろうが更新だろが、表示に必要なパラメーターは変わらないので、この時点でまとめて指定
    context = {
        "form": form,
        "talk": talk,
        "friend": friend,
    }

    # POST（メッセージ送信あり）
    if request.method == "POST":
        # 送信内容を取得
        new_talk = Talk(talk_from=user, talk_to=friend)
        form = TalkForm(request.POST, instance=new_talk)

        # 送信内容があった場合
        if form.is_valid():
            # 保存
            form.save()
            # 更新
            # このようなリダイレクト処理はPOSTのリクエストを初期化し、リクエストをGETに戻すことにより
            # 万一更新処理を連打されてもPOSTのままにさせない等の用途がある
            return redirect("talk_room", user_id)
        # バリデーションが通らなかった時の処理を記述
        else:
            # エラー時 form.errors には エラー内容が格納されている
            print(form.errors)

    # POSTでない（リダイレクトorただの更新）&POSTでも入力がない場合
    return render(request, "myapp/talk_room.html", context)


@login_required
def setting(request):
    return render(request, "myapp/setting.html")


# setting以下のchange系の関数は
# request.methodが"GET"か"POST"かで明示的に分けています。
# これはformの送信があった時とそうで無いときを区別しています。


@login_required
def user_img_change(request):
    user = request.user
    if request.method == "GET":
        # モデルフォームには `instance=user` をつけることで user の情報が入った状態のフォームを参照できます。
        # 今回はユーザ情報の変更の関数が多いのでこれをよく使います。
        form = ImageSettingForm(instance=user)

    elif request.method == "POST":
        form = ImageSettingForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user_img_change_done")
        # バリデーションが通らなかった時の処理を記述
        else:
            # エラー時 form.errors には エラー内容が格納されている
            print(form.errors)

    context = {
        "form": form,
    }
    return render(request, "myapp/user_img_change.html", context)


@login_required
def user_img_change_done(request):
    return render(request, "myapp/user_img_change_done.html")


@login_required
def mail_change(request):
    user = request.user
    if request.method == "GET":
        form = MailSettingForm(instance=user)

    elif request.method == "POST":
        form = MailSettingForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("mail_change_done")
        # バリデーションが通らなかった時の処理を記述
        else:
            # エラー時 form.errors には エラー内容が格納されている
            print(form.errors)

    context = {
        "form": form,
    }
    return render(request, "myapp/mail_change.html", context)


@login_required
def mail_change_done(request):
    return render(request, "myapp/mail_change_done.html")


@login_required
def username_change(request):
    user = request.user
    if request.method == "GET":
        form = UserNameSettingForm(instance=user)

    elif request.method == "POST":
        form = UserNameSettingForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("username_change_done")
        # バリデーションが通らなかった時の処理を記述
        else:
            # エラー時 form.errors には エラー内容が格納されている
            print(form.errors)

    context = {
        "form": form,
    }
    return render(request, "myapp/username_change.html", context)


@login_required
def username_change_done(request):
    return render(request, "myapp/username_change_done.html")


class PasswordChange(PasswordChangeView):
    """Django標準パスワード変更ビュー

    Attributes:
        template_name: 表示するテンプレート
        success_url: 処理が成功した時のリダイレクト先
        form_class: パスワード変更フォーム
    """

    form_class = PasswordChangeForm
    success_url = reverse_lazy("password_change_done")
    template_name = "myapp/password_change.html"


class PasswordChangeDone(PasswordChangeDoneView):
    """Django標準パスワード変更後ビュー"""
