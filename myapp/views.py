from enum import Enum
from django.shortcuts import redirect, render
from django.contrib.auth.password_validation import validate_password  # 以下追記箇所(6～7行目)
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from .models import CustomUser, TalkContent
from .forms import (
    MyUserForm,
    myLoginForm,
    ChatInputForm,
    ChangeUserForm,
    ChangeEmailForm,
    ChangeIconForm,
    ChangePWForm,
)
from django.contrib.auth.views import LoginView
from django.db.models import Q
from PIL import Image


# NOTE: print文はデプロイ時は削除しましょう！→パフォーマンス悪化につながります。
# NOTE:トリミングえらい。
# NOTE:関数わけえらい。
# NOTE: trimming_squareという名前なら、関数内でsaveなど他のことをしない。副作用のない関数を目指す。
def trimming_square(img_path):
    img = Image.open(img_path)
    new_size = min(img.width, img.height)
    center_x = int(img.width / 2)
    center_y = int(img.height / 2)

    img_crop = img.crop(
        (
            center_x - new_size / 2,
            center_y - new_size / 2,
            center_x + new_size / 2,
            center_y + new_size / 2,
        )
    )
    img_crop.save(img_path)


def index(request):
    return render(request, "myapp/index.html")


def signup_view(request):
    if request.method == "POST":
        form = MyUserForm(request.POST, request.FILES)
        if form.is_valid():
            new_username = request.POST["username"]

            cleaned_data = form.cleaned_data

            form.save()
            new_user = CustomUser.objects.get(username=cleaned_data.get("username"))
            picpath = new_user.image.path
            trimming_square(picpath)  # 正方形じゃない画像はトリミングする
            return render(request, "myapp/index.html")

        else:
            return render(request, "myapp/signup.html", {"form": form})

    else:
        form = MyUserForm()
        return render(request, "myapp/signup.html", {"form": form})


def login_view(request):
    if request.POST:
        form = myLoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST["username"]
            id = CustomUser.objects.get(username=username).id
            return friends(request, id)

        else:
            return render(request, "myapp/login.html", {"form": form})

    else:
        form = myLoginForm()
        return render(request, "myapp/login.html", {"form": form})


def friends(request, id):
    if id:
        my_username = CustomUser.objects.get(id=id).username

    if request.POST:
        my_username = request.POST["username"]

    my_id = CustomUser.objects.get(username=my_username).id

    user_all = CustomUser.objects.all()
    user_li = []
    for user in user_all:
        # NOTE:admin消しててえらい
        if user.username == my_username or user.username == "admin":
            continue

        # 最後のトークを取ってくる
        # contents = TalkContent.objects.filter(Q(user_to=my_id, user_from=user.id)|Q(user_to=user.id, user_from=my_id))

        # messages = []
        # for content in contents:
        #     if content.chat_content == "":
        #         continue
        #     messages.append({"time": content.time, "message": content.chat_content})
        # # NOTE key使えててえらい。pythonの知識がある。
        # messages = sorted(messages, key=lambda x: x['time'])
        # if len(messages) == 0:
        #     lasttalk = ""
        # else:
        #     lasttalk = messages[-1]['message']

        # ORMで並び変える方が、pythonのメモリ上で並び替えるより早い。
        # NOTE: 本当はDjangoORMのannotateという機能を使った方が良いが、最適化の時に学んでください。
        last_talk = (
            TalkContent.objects.filter(
                Q(user_to=my_id, user_from=user.id)
                | Q(user_to=user.id, user_from=my_id)
            )
            .order_by("time")
            .last()
        )
        user_li.append(
            {
                "username": user.username,
                "image": user.image.url,
                "id": user.id,
                "lasttalk": last_talk,
            }
        )

    return render(
        request,
        "myapp/friends.html",
        {"id": my_id, "username": my_username, "friends": user_li},
    )


# TODO: id1 は不要、rquestオブジェクトからログイン中のユーザー＝自分自身を取得できる。
def talk_room(request, id1, id2):
    from_user = request.user.username
    to_user = CustomUser.objects.get(id=id2).username

    if request.POST:
        chat_content = request.POST["chat_content"]
        new_message = ChatInputForm(
            {
                "user_from": id1,
                "user_to": id2,
                "chat_content": chat_content,
            }
        )
        if new_message.is_valid():
            new_message.save()
    # talkroom 表示
    contents = TalkContent.objects.filter(
        Q(user_to=id1, user_from=id2) | Q(user_to=id2, user_from=id1)
    ).order_by("time")

    # TODO: 細かい修正は割愛するが、templateに渡すcontextにオブジェクトの配列を入れ込む時、querysetを入れた方が良い。
    # 並び替え等はquerysetのメソッドでできる。
    messages = []
    for content in contents:
        if content.chat_content == "":
            continue
        messages.append(
            {
                "time": content.time,
                "from": CustomUser.objects.get(id=content.user_from).username,
                "to": CustomUser.objects.get(id=content.user_to).username,
                "message": content.chat_content,
            }
        )
    messages = sorted(messages, key=lambda x: x["time"])

    form = ChatInputForm()
    data = {
        "myusername": from_user,
        "myid": id1,
        "your_id": id2,
        "to_username": to_user,
        "messages": messages,
        "form": form,
    }
    return render(request, "myapp/talk_room.html", data)


class SettingChoice(Enum):
    USER_NAME = 1
    EMAIL = 2
    ICON = 3
    PASSWORD = 4


# TODO:一つのエンドポイントでいくつもの機能を実装するような設計は良くなさそう。
# パラメーターで分岐するのではなくそれぞれでページを分けた方が可読性の高いコードになる。
def setting(request, id, what):
    data = {"id": id, "what": what}
    now_user = CustomUser.objects.get(id=id)
    username = now_user.username

    # default
    # TODO: switch分の方が良いかも。
    # TODO: enumを使うとめっちゃわかりやすそう。
    if what == 0:
        return render(request, "myapp/setting.html", data | {"content": "Username"})

    # change username
    if SettingChoice.USER_NAME.value == 1:
        if request.POST:
            new = request.POST["username"]
            form = ChangeUserForm(request.POST)

            if form.is_valid():
                now_user.username = new
                now_user.save()
                return render(
                    request,
                    "myapp/change_complete.html",
                    data | {"content": "Username"},
                )
            else:
                return render(
                    request,
                    "myapp/setting_change.html",
                    data | {"form": form, "content": "Username"},
                )
        else:
            form = ChangeUserForm()
            return render(
                request,
                "myapp/setting_change.html",
                data | {"form": form, "content": "Username"},
            )

    # change email address
    if SettingChoice.EMAIL.value == 2:
        if request.POST:
            new = request.POST["email"]
            form = ChangeEmailForm(request.POST)

            if form.is_valid():
                now_user.email = new
                now_user.save()
                return render(
                    request, "myapp/change_complete.html", data | {"content": "Email"}
                )
            else:
                return render(
                    request,
                    "myapp/setting_change.html",
                    data | {"form": form, "content": "Email"},
                )
        else:
            form = ChangeEmailForm()
            return render(
                request,
                "myapp/setting_change.html",
                data | {"form": form, "content": "Email"},
            )

    # change icon
    if SettingChoice.ICON.value == 3:
        if request.POST:
            new = request.FILES["image"]
            form = ChangeIconForm(request.POST, request.FILES)

            if form.is_valid():
                now_user.image = new
                now_user.save()
                picpath = now_user.image.url
                trimming_square("./" + picpath[1:])  # 正方形じゃない画像はトリミングする
                return render(
                    request, "myapp/change_complete.html", data | {"content": "Icon"}
                )
            else:
                return render(
                    request,
                    "myapp/setting_change.html",
                    data | {"form": form, "content": "Icon"},
                )
        else:
            form = ChangeIconForm()
            return render(
                request,
                "myapp/setting_change.html",
                data | {"form": form, "content": "Icon"},
            )

        pass
    # change password
    if SettingChoice.PASSWORD.value == 4:
        # えらい
        form = ChangePWForm(user=now_user, data=request.POST)
        if request.POST:
            if form.is_valid():
                form.save()
                return render(
                    request,
                    "myapp/change_complete.html",
                    data | {"content": "Password"},
                )
            else:
                return render(
                    request,
                    "myapp/setting_change.html",
                    data | {"form": form, "content": "Password"},
                )

        else:
            form = ChangePWForm(user=now_user)
            return render(
                request,
                "myapp/setting_change.html",
                data | {"form": form, "content": "Password"},
            )

    return render(request, "myapp/setting.html", data)
