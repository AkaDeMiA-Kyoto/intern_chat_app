import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import F, Q
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import (
    LoginForm,
    MessageForm,
    ProfImageForm,
    SearchForm,
    SignUpForm,
    UserNameForm,
)
from .models import CustomMessage, CustomUser


def index(request):
    return render(request, "myapp/index.html")


def signup_view(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("index")
        else:
            print("Form is not Valid!")
            for err in form.errors:
                print(err)
            return render(request, "myapp/signup.html", {"form": form})

    return render(request, "myapp/signup.html", {"form": form})


@login_required
def friends(request):
    data = CustomUser.objects.all()
    form = SearchForm(request.POST)
    hasFormContent = False
    if request.method == "POST" and request.POST["content"] != "":
        if "btn_reset" in request.POST:
            # フォームクリアボタンの処理。
            form = SearchForm()
        elif request.POST["content"] != "":
            searchName = request.POST["content"]
            hasFormContent = True
            if request.POST["searchOption"] == "0":
                # ユーザー名での検索処理(部分一致を許す)
                data = data.filter(username__contains=searchName)
            elif request.POST["searchOption"] == "1":
                # メールアドレスでの検索処理(完全一致のみ)
                data = data.filter(email=searchName)

    # メッセージ取得、ソート
    myMsg = request.user.msg.all().order_by(F("createdTime"))

    # 表示順
    friendOrder = {}
    for friend in data:
        friendOrder[friend.id] = friend.date_joined + datetime.timedelta(weeks=-20000)
    for msg in myMsg:
        friendOrder[msg.subUser_id] = msg.createdTime

    # テンプレートに渡す用
    friends = []
    for friend in data:
        if friend.id == request.user.id:
            continue
        # 画像URL、なければ置き換え
        # prof_img_url = "media/null_img.png"
        prof_img_url = None
        if friend.prof_img:
            prof_img_url = friend.prof_img.url

        # リストに追加
        friends.append(
            {
                "id": friend.id,
                "username": friend.username,
                "prof_img_url": prof_img_url,
                "order": friendOrder[friend.id],
            }
        )
    friends.sort(key=lambda x: x["order"], reverse=True)

    hasData = data.count() > 0
    params = {
        "form": form,
        "hasData": hasData,
        "data": friends,
        "hasFormContent": hasFormContent,
    }
    return render(request, "myapp/friends.html", params)


@login_required
def talk_room(request, talkee):
    # 存在しないIDのページにアクセスした場合
    if CustomUser.objects.filter(id=talkee).first() is None:
        return render(request, "myapp/talk_room.html", {"isValidUrl": False})

    # フォーム、ID、画像登録
    mform = MessageForm()
    myImg = "myapp/img/nullImage"
    if request.user.prof_img:
        myImg = request.user.prof_img.url
    # if (CustomUser.objects.get(id=myid).prof_img):
    #    myImg=CustomUser.objects.get(id=myid).prof_img.url
    theirImg = "myapp/img/nullImage"
    them = CustomUser.objects.get(id=talkee)
    if them.prof_img:
        theirImg = them.prof_img.url

    # メッセージ送信
    if request.method == "POST":
        msgTime = timezone.now().isoformat()
        msgContent = request.POST["content"]
        msg = CustomMessage(
            content=msgContent,
            primeUser=request.user,
            subUser=them,
            isReceipt=False,
            createdTime=msgTime,
        )
        msg.save()
        dummyMsg = CustomMessage(
            content=msgContent,
            primeUser=them,
            subUser=request.user,
            isReceipt=True,
            createdTime=msgTime,
        )
        dummyMsg.save()

    # メッセージ取得、ソート
    msgraw = request.user.msg.filter(Q(subUser=them)).order_by(F("createdTime"))
    # 表示
    dic = {
        "isValidUrl": True,
        "self": talkee,
        "name": them.username,
        "form": mform,
        "msg": msgraw,
        "myImg": myImg,
        "theirImg": theirImg,
    }
    return render(request, "myapp/talk_room.html", dic)


@login_required
def setting(request):
    return render(request, "myapp/setting.html")


@login_required
def changeUserName(request):
    form = UserNameForm(request.POST)
    err = ""
    if request.method == "POST":
        if form.is_valid() or request.POST["username"] == request.user.username:
            form = UserNameForm(request.POST, instance=request.user)
            form.save()
            return redirect("setting")
        else:
            err = form.errors
    dic = {"title": "Change User Name", "form": form, "err": err}
    return render(request, "myapp/simpleform.html", dic)


@login_required
def changeProfImg(request):
    form = ProfImageForm(request.FILES)
    err = ""
    if request.method == "POST":
        if form.is_valid:
            form = ProfImageForm(request.POST, request.FILES, instance=request.user)
            form.save()
            return redirect("setting")
        else:
            form = ProfImageForm(request.FILES)
            err = form.errors

    dic = {"title": "Change Profile Image", "form": form, "err": err}
    return render(request, "myapp/simpleform.html", dic)


class MyLoginView(LoginView):
    authentication_form = LoginForm
    template_name = "myapp/login.html"


class Logout(LogoutView, LoginRequiredMixin):
    template_name = "myapp/logout.html"
