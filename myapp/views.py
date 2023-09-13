from django.shortcuts import redirect, render
from django.contrib.auth.password_validation import validate_password # 以下追記箇所(6～7行目)
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import *
from django.contrib.auth.views import LoginView
from django.db.models import Q
from PIL import Image
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

def trimming_square(imgpath):
    img = Image.open(imgpath)
    new_size = min(img.width, img.height)
    center_x = int(img.width / 2)
    center_y = int(img.height / 2)

    img_crop = img.crop((center_x - new_size / 2, center_y - new_size / 2, center_x + new_size / 2, center_y + new_size / 2))
    img_crop.save(imgpath)



def index(request):
    print("user: ",request.user.username)
    if request.user.username == '':
        return render(request, "myapp/index.html")
    else:
        return friends(request)
    
def logout_view(request):
    logout(request)
    return index(request)

def signup_view(request):
    if request.POST:
        form = myUserForm(request.POST, request.FILES)

        if form.is_valid():
            print("************VALID*********************")
            new_username = request.POST["username"]

            data = form.cleaned_data

            form.save()
            new_user = CustomUser.objects.get(username=new_username)
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
            user = CustomUser.objects.get(username=username)
            login(request, form.get_user())
            id = user.id
            print("******", id)
            return friends(request)

        else:
            print("************Login Failed*********************")
            return render(request, "myapp/login.html", {'form': form})
    
    else:
        print("******************NOT POST *****************")
        form = myLoginForm()
        return render(request, "myapp/login.html", {'form': form})

@login_required
def friends(request):
    myid = request.user.id
    if id:
        myusername = CustomUser.objects.get(id=myid).username

    if request.POST:
        myusername = request.POST["username"]

    user_all = CustomUser.objects.all()    
    user_li = []
    for user in user_all:
        if user.username == myusername or user.username == 'admin':
            continue
        print("*** user: ", user.username)
        # 最後のトークを取ってくる 
        contents = Talk_content.objects.filter(Q(user_to=myid, user_from=user.id)|Q(user_to=user.id, user_from=myid))

        messages = []
        for content_ in contents:
            if content_.chat_content == "":
                continue
            messages.append({"time": content_.time, "message": content_.chat_content})
        messages = sorted(messages, key=lambda x: x['time'])
        if len(messages) == 0:
            lasttalk = ""
        else:
            lasttalk = messages[-1]['message']
        print("image url: ",user.image)
        trimming_square("./"+ user.image.url[1:]) # 正方形じゃない画像はトリミングする
        user_li.append({"username": user.username, "image": user.image.url, "id": user.id, "lasttalk": lasttalk})

    search_form = SearchFriendForm()
    return render(request, "myapp/friends.html", {"id": myid, "username": myusername, "friends": user_li, "search_form": search_form})

@login_required
def search_friends(request):
    myid = request.user.id
    myusername = CustomUser.objects.get(id=myid).username

    if request.POST:
        search_form = SearchFriendForm(request.POST)

        search_name = request.POST["username"]
        print("*****search_name : ", search_name)
        if search_name == "":
            return friends(request)
        
        detected_user = CustomUser.objects.filter(username__icontains=search_name).all()

        user_li = []
        for user in detected_user:
            print(user.username)
            if user.username == myusername or user.username == 'admin':
                continue
            
            # 最後のトークを取ってくる 
            contents = Talk_content.objects.filter(Q(user_to=myid, user_from=user.id)|Q(user_to=user.id, user_from=myid))

            messages = []
            for content_ in contents:
                if content_.chat_content == "":
                    continue
                messages.append({"time": content_.time, "message": content_.chat_content})
            messages = sorted(messages, key=lambda x: x['time'])
            if len(messages) == 0:
                lasttalk = ""
            else:
                lasttalk = messages[-1]['message']
            print("image url: ",user.image)
            trimming_square("./"+ user.image.url[1:]) # 正方形じゃない画像はトリミングする
            user_li.append({"username": user.username, "image": user.image.url, "id": user.id, "lasttalk": lasttalk})

        return render(request, "myapp/friends.html", {"id": myid, "username": myusername, "friends": user_li, "search_form": search_form})

    return friends(request)


@login_required
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
    for content_ in contents:
        if content_.chat_content == "":
            continue
        messages.append({"time": content_.time, "from": CustomUser.objects.get(id=content_.user_from).username, "to": CustomUser.objects.get(id=content_.user_to).username, "message": content_.chat_content})
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

@login_required
def setting(request, what):
    id = request.user.id
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