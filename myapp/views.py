import operator

from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
)
from django.db.models import Q
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
    """ログインページ

    GETの時は指定されたformを指定したテンプレートに表示
    POSTの時はloginを試みる。→成功すればdettingのLOGIN_REDIRECT_URLで指定されたURLに飛ぶ
    """

    authentication_form = LoginForm
    template_name = "myapp/login.html"


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""


@login_required
def friends(request):
    user = request.user
    friends = User.objects.exclude(id=user.id)

    # トーク情報とフレンド情報を含む info を作成
    info = []
    info_have_message = []
    info_have_no_message = []
    
    for friend in friends:
        # 最新のメッセージの取得
        latest_message = Talk.objects.filter(
            Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend)
        ).order_by('time').last()

        if latest_message:
            info_have_message.append([friend, latest_message.talk, latest_message.time])
        else:
            info_have_no_message.append([friend, None, None])
    
    # 時間順に並び替え
    info_have_message = sorted(info_have_message, key=operator.itemgetter(2), reverse=True)
    
    info.extend(info_have_message)
    info.extend(info_have_no_message)
    
    context = {
        "info": info,
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
