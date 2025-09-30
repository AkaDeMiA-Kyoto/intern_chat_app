import operator
import secrets

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
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.conf import settings
import unicodedata
from django.db.models.functions import Substr, StrIndex
from django.db import models
from django.db.models.functions import StrIndex, Substr
from .models import Talk
import unicodedata
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Q, OuterRef, Subquery, F, Value, Case, When, CharField
from django.db.models import OuterRef, Subquery

from .forms import (
    ImageSettingForm,
    LoginForm,
    MailSettingForm,
    PasswordChangeForm,
    SignUpForm,
    TalkForm,
    UserNameSettingForm,
)
from .models import Talk, TwoFactorCode

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
            # つまり、autenticateメソッドは"username"と"password"を受け取り、その組み合わせが存在すれば
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
    authentication_form = LoginForm
    template_name = "myapp/login.html"
    def form_valid(self, form):
        user = form.get_user()
        self.request.session['user_id'] = user.id
        generate_and_send_code(user)
        return redirect('verify_code')


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""


@login_required
def friends(request):
    user = request.user

    latest_talk_qs = (
        Talk.objects
        .filter(
            Q(talk_from=user, talk_to=OuterRef("pk")) |
            Q(talk_to=user, talk_from=OuterRef("pk"))
        )
        .order_by("-time")
    )

    friends_qs = (
        User.objects
        .exclude(id=user.id)
        .annotate(
            latest_talk_text=Subquery(latest_talk_qs.values("talk")[:1]),
            latest_talk_time=Subquery(latest_talk_qs.values("time")[:1]),
        )
    )

    info = [(f, f.latest_talk_text, f.latest_talk_time) for f in friends_qs]

    info.sort(key=lambda x: (x[2] is None, x[2] or 0))

    return render(request, "myapp/friends.html", {"info": info})


@login_required
def talk_room(request, user_id):
    # ユーザ・友達をともにオブジェクトで取得
    user = request.user
    friend = get_object_or_404(User, id=user_id)
    # 自分→友達、友達→自分のトークを全て取得
    talk = (Talk.objects
        .filter(Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend))
        .select_related("talk_from", "talk_to")                     
        .only("talk", "time", "talk_from__username", "talk_to__username")
        .order_by("time"))
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

def generate_and_send_code(user):
    code = str(secrets.randbelow(1000000)).zfill(6)

    two_factor_code, created = TwoFactorCode.objects.update_or_create(
        user=user,
        defaults={'code': code}
    )

    subject = '2段階認証コード'
    message = f'認証コードは {code} です。'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


def verify_code(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        if not user_id:
            messages.error(request, 'セッション情報が無効です。再度ログインしてください。')
            return redirect('login')
        entered_code = request.POST.get('code')

        try:
            two_factor_code = TwoFactorCode.objects.get(user=user)
            if two_factor_code.code == entered_code and not two_factor_code.is_expired():
                login(request, user)
                two_factor_code.delete()
                del request.session['user_id']
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                messages.error(request, '無効なコードです。')
        except TwoFactorCode.DoesNotExist:
            messages.error(request, '無効なコードです。')

    return render(request, 'myapp/verify_code.html')

def _tokens(q: str):
    q = unicodedata.normalize("NFKC", (q or "")).strip().replace("\u3000", " ")
    return [t for t in q.split(" ") if t]

def user_search_view(request):
    User = get_user_model()
    raw_q = request.GET.get("q", "")
    toks = _tokens(raw_q)

    info = []
    if toks:
        base = (
            User.objects
            .annotate(at_pos=StrIndex("email", Value("@")))
            .annotate(
                email_local=Case(
                    When(at_pos__gt=1, then=Substr("email", 1, F("at_pos") - 1)),
                    default=Value(""),
                    output_field=CharField(),
                )
            )
            .filter(is_active=True)
            .exclude(pk=request.user.pk)
        )

        cond = Q()
        for t in toks:
            per_tok = (
                Q(username__icontains=t) |
                Q(first_name__icontains=t) |
                Q(last_name__icontains=t) |
                Q(email_local__icontains=t)
            )
            cond &= per_tok

        qs = base.filter(cond)

        latest = Talk.objects.filter(
            Q(talk_from=request.user, talk_to=OuterRef('pk')) |
            Q(talk_from=OuterRef('pk'), talk_to=request.user)
        ).order_by('-time')

        qs = qs.annotate(
            last_talk=Subquery(latest.values('talk')[:1]),
            last_time=Subquery(latest.values('time')[:1]),
        ).order_by('username').distinct()

        info = [(u, u.last_talk, u.last_time) for u in qs]

    return render(request, 'myapp/friends.html', {
        'info': info,
        'query': raw_q,
    })