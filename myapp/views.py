import operator

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.db.models import F
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
)
from django.db.models import Q, OuterRef, Subquery 
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from .forms import (
    ImageSettingForm,
    LoginForm,
    MailSettingForm,
    UserPasswordChange,
    SignUpForm,
    TalkForm,
    UserNameSettingForm,
    TwoFactorForm,
)
from .models import Talk,EmailOTP

User = get_user_model()



def index(request):
    return render(request, "myapp/index.html")


def signup_view(request):
    if request.method == "GET":
        form = SignUpForm()
        error_message = ''
    elif request.method == "POST":
        # 画像ファイルをformに入れた状態で使いたい時はformに"request.FILES"を加える。
        # request.POST だけではNoneが入る。
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            # モデルフォームはformの値をmodelsにそのまま格納できるsave()メソッドがあるので便利。
            form.save()
            # フォームから"username"を読み取る
            username = form.cleaned_data.get("username")
            # フォームから"password1"を読み取る
            password = form.cleaned_data.get("password1")
            # 認証情報のセットを検証するには authenticate() を利用してください。
            # このメソッドは認証情報をキーワード引数として受け取ります。
            # 検証する対象はデフォルトでは username と password であり
            # その組み合わせを個々の 認証バックエンド に対して問い合わせ、認証バックエンドで認証情報が有効とされれば
            # User オブジェクトを返します。もしいずれの認証バックエンドでも認証情報が有効と判定されなければ PermissionDenied が送出され、None が返されます。
            # (公式ドキュメントより)
            # つまり、authenticateメソッドは"username"と"password"を受け取り、その組み合わせが存在すれば
            # そのUserを返し、不正であれば"None"を返します。
            user = authenticate(username=username, password=password)
            if user is not None:
                # あるユーザーをログインさせる場合は、login() を利用してください。この関数は HttpRequest オブジェクトと User オブジェクトを受け取ります。
                # ここでのUserは認証バックエンド属性を持ってる必要がある。
                # authenticate()が返すUserはuser.backendを持つので連携可能。
                login(request, user)
            return redirect("/")
        # バリデーションが通らなかった時の処理を記述
        else:
            # エラー時 form.errors には エラー内容が格納されている
            print(form.errors)

            

    context = {
        "form": form,
    }
    return render(request, "myapp/signup.html", context)


class Login(LoginView):
    """ログインページ

    GETの時は指定されたformを指定したテンプレートに表示
    POSTの時はloginを試みる。→成功すればdettingのLOGIN_REDIRECT_URLで指定されたURLに飛ぶ
    """

    authentication_form = LoginForm
    template_name = "myapp/login.html"

    def form_valid(self, form):
        user = form.get_user()

        if not user.email:
            form.add_error(None, "このアカウントにメールアドレスが登録されていません。")
            return self.form_invalid(form)


        otp = EmailOTP.create_for(user, ttl_minutes=10)
        send_mail(
            subject="【ログイン確認】パスコード",
            message=f"パスコード: {otp.code}\n有効期限: 10分",
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            recipient_list=[user.email],
            fail_silently=False,
        )

        self.request.session["2fa_user_id"] = user.id
        nxt = self.request.POST.get("next") or self.request.GET.get("next")
        if nxt:
            self.request.session["2fa_next"] = nxt

        messages.info(self.request, "パスコードをメールに送信しました。10分以内に入力してください。")
        return redirect("two_factor_verify")  # 2FA入力画面へ

def two_factor_verify_view(request):
    user_id = request.session.get("2fa_user_id")
    if not user_id:
        messages.warning(request, "まずユーザー名とパスワードを入力してください。")
        return redirect("login_view")  

    User = get_user_model()
    user = User.objects.get(id=user_id)
    otp = EmailOTP.objects.filter(user=user, is_used=False).order_by("-created_at").first()

    if request.method == "POST":
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            if (otp is None) or (not otp.is_valid_now()):
                form.add_error(None, "コードが無効か期限切れです。はじめからやり直してください。")
            elif code != otp.code:
                EmailOTP.objects.filter(pk=otp.pk).update(attempts=F("attempts") + 1)
                otp.refresh_from_db()
            else:
                otp.is_used = True
                otp.save(update_fields=["is_used"])
                login(request, user)

                next_url = request.session.pop("2fa_next", None)
                request.session.pop("2fa_user_id", None)
                return redirect(next_url or self_success_url_fallback())

    else:
        form = TwoFactorForm()

    return render(request, "myapp/two_factor.html", {"form": form, "user_email": user.email})

def self_success_url_fallback():
    from django.conf import settings
    return getattr(settings, "LOGIN_REDIRECT_URL", "/")

def two_factor_resend_view(request):
    user_id = request.session.get("2fa_user_id")
    if not user_id:
        messages.warning(request, "まずユーザー名とパスワードを入力してください。")
        return redirect("login_view")

    User = get_user_model()
    user = User.objects.get(id=user_id)

    otp = EmailOTP.create_for(user, ttl_minutes=10)
    send_mail(
        subject="【ログイン確認】パスコード（再送）",
        message=f"パスコード: {otp.code}\n有効期限: 10分",
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
        recipient_list=[user.email],
        fail_silently=False,
    )
    messages.info(request, "パスコードを再送しました。")
    return redirect("two_factor_verify")


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""


@login_required
def friends(request):
    me = request.user
    q = (request.GET.get("q") or "").strip()

    friends_qs = User.objects.exclude(pk=me.pk)
    if q:
        friends_qs = friends_qs.filter(username__icontains=q)

    talks_between = (Talk.objects
        .filter(Q(talk_from=me, talk_to=OuterRef("pk")) | Q(talk_from=OuterRef("pk"), talk_to=me))
        .order_by("-time"))

    friends_qs = friends_qs.annotate(
        latest_time=Subquery(talks_between.values("time")[:1]),
        latest_text=Subquery(talks_between.values("talk")[:1]),
    )

    info_have_message = []
    info_have_no_message = []
    for friend in friends_qs:
        lt = getattr(friend, "latest_time", None)
        lx = getattr(friend, "latest_text", None)
        if lt:
            info_have_message.append([friend, lx, lt])
        else:
            info_have_no_message.append([friend, None, None])

    info_have_message = sorted(info_have_message, key=operator.itemgetter(2), reverse=True)

    info = []
    info.extend(info_have_message)
    info.extend(info_have_no_message)
    
    context = {
        "info": info,
    }
    return render(request, "myapp/friends.html", context)

def get_queryset(user, friend):
    return (Talk.objects
            .filter(Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend))
            .select_related("talk_from", "talk_to")  
            .order_by("time"))

@login_required
def talk_room(request, user_id):
    user = request.user
    friend = get_object_or_404(User, id=user_id)

    talk = get_queryset(user, friend)

    form = TalkForm()
    context = {
        "form": form,
        "talk": talk,
        "friend": friend,
    }

    if request.method == "POST":
        new_talk = Talk(talk_from=user, talk_to=friend)
        form = TalkForm(request.POST, instance=new_talk)
        if form.is_valid():
            form.save()
            return redirect("talk_room", user_id=friend.id)
        else:
            print(form.errors)

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

    form_class = UserPasswordChange
    success_url = reverse_lazy("password_change_done")
    template_name = "myapp/password_change.html"


class PasswordChangeDone(PasswordChangeDoneView):
    """Django標準パスワード変更後ビュー"""
    template_name = "myapp/password_change_done.html"