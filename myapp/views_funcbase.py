from django.shortcuts import redirect, render
from django.contrib.auth.password_validation import validate_password # 以下追記箇所(6～7行目)
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import *
from django.contrib.auth.views import LoginView
from django.db.models import Q, F, OuterRef, Subquery
from PIL import Image
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings

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
        return redirect('friends')#friends(request)
    
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
            return redirect('friends')#friends(request)

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
    myusername = request.user.username

    lastmsg = Talk_content.objects.filter(
            Q(user_to=request.user, user_from=OuterRef('pk'))|Q(user_to=OuterRef('pk'), user_from=request.user)
        ).order_by("-time")
    user_li = list(
        CustomUser.objects.filter(~Q(username=myusername) & ~Q(username='admin')).annotate(
            lasttalk = Subquery(lastmsg.values('chat_content')[:1]),
        )
    )

    search_form = SearchFriendForm()
    return render(request, "myapp/friends.html", {"id": myid, "username": myusername, "friends": user_li, "search_form": search_form})

@login_required
def search_friends(request):
    myid = request.user.id
    myusername = request.user.username

    if request.POST:
        search_form = SearchFriendForm(request.POST)

        search_name = request.POST["username"]
        print("*****search_name : ", search_name)
        
        lastmsg = Talk_content.objects.filter(
            Q(user_to=request.user, user_from=OuterRef('pk'))|Q(user_to=OuterRef('pk'), user_from=request.user)
        ).order_by("-time")
        user_li = list(
            CustomUser.objects.filter(Q(username__icontains=search_name)).annotate(
                lasttalk = Subquery(lastmsg.values('chat_content')[:1]),
            )
        )

        return render(request, "myapp/friends.html", {"id": myid, "username": myusername, "friends": user_li, "search_form": search_form})

    return friends(request)


@login_required
def talk_room(request, id1, id2):
    user1 = CustomUser.objects.get(id=id1)
    user2 = CustomUser.objects.get(id=id2)

    if request.POST:
        chat_content = request.POST["chat_content"]
        new_message = ChatInputForm({"user_from": user1, "user_to": user2, "chat_content": chat_content})
        if new_message.is_valid():
            print("***MESSAGE VALID******")
            new_message.save()
        else:
            print("***MESSAGE INAVLID***")

    # talkroom 表示
    messages= list(
        Talk_content.objects.filter(
            (Q(user_to=user1, user_from=user2) | Q(user_to=user2, user_from=user1)) & ~Q(chat_content="") 
        ).order_by('time').values('time', 'user_from__username', 'user_to__username', 'chat_content') 
    )
    form = ChatInputForm()
    data = {
        "I": user1,
        "You": user2,
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
        return render(request, "myapp/setting_funcbase.html", data | {"content": "Username"})
    
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
                return render(request, "myapp/setting_change_funcbase.html", data | {"form": form, "content": "Username"})
        else:
            form = ChangeUserForm()
            return render(request, "myapp/setting_change_funcbase.html", data | {"form": form, "content": "Username"})
    
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
                return render(request, "myapp/setting_change_funcbase.html", data | {"form": form, "content": "Email"})
        else:
            form = ChangeEmailForm()
            return render(request, "myapp/setting_change_funcbase.html", data | {"form": form, "content": "Email"})

    # change icon   
    if what == 3: 
        if request.POST:
            new = request.FILES["image"]
            form = ChangeIconForm(request.POST, request.FILES)

            if form.is_valid():
                print("********VALID*********")
                now_user.image = new
                now_user.save()
                picpath = now_user.image.url
                # trimming_square("./"+picpath[1:]) # 正方形じゃない画像はトリミングする
                return render(request, "myapp/change_complete.html", data | {"content": "Icon"})
            else:
              return render(request, "myapp/setting_change_funcbase.html", data | {"form": form, "content": "Icon"})
        else:
            form = ChangeIconForm()
            return render(request, "myapp/setting_change_funcbase.html", data | {"form": form, "content": "Icon"})

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
                return render(request, "myapp/setting_change_funcbase.html", data | {"form": form, "content": "Password"})

        else:
            form = ChangePWForm(user=now_user)
            return render(request, "myapp/setting_change_funcbase.html", data | {"form": form, "content": "Password"})

    return render(request, "myapp/setting_funcbase.html", data)