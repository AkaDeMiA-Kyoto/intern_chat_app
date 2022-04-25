from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordChangeDoneView,
    PasswordChangeView,
)
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from .forms import (
    ImageSettingForm,
    PasswordChangeForm,
    TalkForm,
    UserNameSettingForm,
    FriendsSearchForm
)
from .models import Talk
from .utils import create_info_list # よく使う関数は utils 等に切り分ける

User = get_user_model()


def index(request):
    return render(request, "myapp/index.html")


@login_required
def friends(request):
    user = request.user
    friends = User.objects.exclude(id=user.id)

    info = create_info_list(user, friends)
    
    # 検索機能
    form = FriendsSearchForm()

    if request.method == "GET" and "friends_search" in request.GET:
        form = FriendsSearchForm(request.GET)

        # 送信内容があった場合
        if form.is_valid():
            keyword = form.cleaned_data.get("keyword")
            # 何も入力せずに検索した時に全件を表示するようにするため、分岐しておく
            if keyword:
                # 入力に対して部分一致する友達を絞り込む
                friends = friends.filter(username__icontains=keyword)

                # 検索に対してリストを作成
                info = create_info_list(user, friends)

                # friendsに何らか情報があったとき
                context = {
                    "info": info,
                    "form": form,
                    # 検索結果を表示する画面にするために、そうであることを明示する変数を作る
                    "is_searched": True,
                }
                return render(request, "myapp/friends.html", context)


    
    # ここまで検索機能

    context = {
        "info": info,
        "form": form,
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
            return redirect("talk_room", user_id)

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
    context = {
        "form": form,
    }
    return render(request, "myapp/user_img_change.html", context)


@login_required
def user_img_change_done(request):
    return render(request, "myapp/user_img_change_done.html")


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

