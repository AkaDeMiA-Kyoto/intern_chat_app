from django.shortcuts import redirect, render
from django.contrib.auth.password_validation import validate_password # 以下追記箇所(6～7行目)
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, TalkContent
from .forms import myUserForm, myLoginForm, ChatInputForm, ChangeUserForm, ChangeEmailForm, ChangeIconForm, ChangePWForm
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

    img_crop = img.crop((center_x - new_size / 2, center_y - new_size / 2, center_x + new_size / 2, center_y + new_size / 2))
    img_crop.save(imgpath)

    print("******** Trimming Completed. *************")



def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method=='POST':
        form = myUserForm(request.POST, request.FILES)
        if form.is_valid():
            new_username = request.POST["username"]

            cleaned_data = form.cleaned_data

            form.save()
            new_user = CustomUser.objects.get(username=cleaned_data.get("username"))
            picpath = new_user.image.url
            trimming_square("./"+picpath[1:]) # 正方形じゃない画像はトリミングする


            return render(request, "myapp/index.html")

        else:
            print("************INVALID*********************")
            return render(request, "myapp/signup.html", {'form': form})

    else:
        print("******************NOT POST*****************")
        form = myUserForm()
        return render(request, "myapp/signup.html", {'form': form})

def login_view(request):
    if request.POST:
        form = myLoginForm(request, data=request.POST)

        if form.is_valid():
            print("************Login Sccess*********************")
            username = request.POST["username"]
            id = CustomUser.objects.get(username=username).id
            print("******", id)
            return friends(request, id)

        else:
            print("************Login Failed*********************")
            return render(request, "myapp/login.html", {'form': form})
    
    else:
        print("******************NOT POST *****************")
        form = myLoginForm()
        return render(request, "myapp/login.html", {'form': form})

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
        if user.username == my_username or user.username == 'admin':
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
        last_talk=TalkContent.objects.filter(Q(user_to=my_id, user_from=user.id)|Q(user_to=user.id, user_from=my_id)).orderby("time").last()
        user_li.append({"username": user.username, "image": user.image.url, "id": user.id, "lasttalk": lasttalk})

    return render(request, "myapp/friends.html", {"id": myid, "username": myusername, "friends": user_li})

def talk_room(request, id1, id2):
    user1 = CustomUser.objects.get(id=id1).username
    user2 = CustomUser.objects.get(id=id2).username

    if request.POST:
        chat_content = request.POST["chat_content"]
        new_message = ChatInputForm({"user_from": id1, "user_to": id2, "chat_content": chat_content})
        if new_message.is_valid():
            print("***VALID******")
            new_message.save()
        else:
            print("***INAVLID***")

            #new_message.save()
    # talkroom 表示
    contents = Talk_content.objects.filter(Q(user_to=id1, user_from=id2)|Q(user_to=id2, user_from=id1))

    messages = []
    for content in contents:
        if content.chat_content == "":
            continue
        messages.append({"time": content.time, "from": CustomUser.objects.get(id=content.user_from).username, "to": CustomUser.objects.get(id=content.user_to).username, "message": content.chat_content})
    messages = sorted(messages, key=lambda x: x['time'])

    form = ChatInputForm()
    data = {
        "myusername": user1,
        "myid": id1,
        "your_id": id2,
        "to_username": user2,
        "messages": messages,
        "form": form
    }
    return render(request, "myapp/talk_room.html", data)

def setting(request, id, what):
    data = {"id": id, "what": what}
    now_user = CustomUser.objects.get(id=id)
    username = now_user.username

    # default
    if what == 0:
        return render(request, "myapp/setting.html", data | {"content": "Username"})
    
    # change username
    if what == 1: 
        if request.POST:
            new = request.POST["username"]
            form = ChangeUserForm(request.POST)

            if form.is_valid():
                print("********VALID*********")
                now_user.username = new
                now_user.save()
                return render(request, "myapp/change_complete.html", data | {"content": "Username"})
            else:
                return render(request, "myapp/setting_change.html", data | {"form": form, "content": "Username"})
        else:
            form = ChangeUserForm()
            return render(request, "myapp/setting_change.html", data | {"form": form, "content": "Username"})
    
    # change email address
    if what == 2: 
        if request.POST:
            new = request.POST["email"]
            form = ChangeEmailForm(request.POST)

            if form.is_valid():
                print("********VALID*********")
                now_user.email = new
                now_user.save()
                return render(request, "myapp/change_complete.html", data | {"content": "Email"})
            else:
                return render(request, "myapp/setting_change.html", data | {"form": form, "content": "Email"})
        else:
            form = ChangeEmailForm()
            return render(request, "myapp/setting_change.html", data | {"form": form, "content": "Email"})

    # change icon   
    if what == 3: 
        if request.POST:
            new = request.FILES["image"]
            print(f"************{new}****")
            form = ChangeIconForm(request.POST, request.FILES)

            if form.is_valid():
                print("********VALID*********")
                now_user.image = new
                now_user.save()
                picpath = now_user.image.url
                trimming_square("./"+picpath[1:]) # 正方形じゃない画像はトリミングする
                return render(request, "myapp/change_complete.html", data | {"content": "Icon"})
            else:
              return render(request, "myapp/setting_change.html", data | {"form": form, "content": "Icon"})
        else:
            form = ChangeIconForm()
            return render(request, "myapp/setting_change.html", data | {"form": form, "content": "Icon"})

        pass
    # change password
    if what == 4:
        form = ChangePWForm(user=now_user, data=request.POST)
        if request.POST:
            print(request.POST, request.user,username)

            if form.is_valid():
                print("********VALID*********")
                form.save()
                return render(request, "myapp/change_complete.html", data | {"content": "Password"})
            else:
                print("********INVALID*********")
                return render(request, "myapp/setting_change.html", data | {"form": form, "content": "Password"})

        else:
            form = ChangePWForm(user=now_user)
            return render(request, "myapp/setting_change.html", data | {"form": form, "content": "Password"})



    return render(request, "myapp/setting.html", data)