
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.http import HttpResponse
from myapp.forms import LoginForm, Setting_img, Setting_mail, Setting_name, Setting_password, SignupForm,TalkroomForm
from myapp.models import CustomUser,Talkroom
from django.utils import timezone
from django.db.models import Q


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    params={
        'form':SignupForm(),
        'errorMessage':""
    }
    if(request.method=="POST"):
        obj = CustomUser()
        form = SignupForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("index")
        else:
            params["errorMessage"]="もう一度情報を入力してください"
            
    return render(request, "myapp/signup.html",params)

def login_view(request):
    params={
        'form':LoginForm(),
        'Errormessage':'',
    }
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            user = CustomUser.objects.get(username=username)
            login(request,user)
            return redirect("friends")
        else:
            params["Errormessage"] = "ユーザーネームとパスワードが一致しません。別の組み合わせをお試しください。"

    return render(request, "myapp/login.html",params)
    
            
        

def friends(request):
    name = request.user.username
    friend_list=CustomUser.objects.exclude(username=name)
    friend_list_1=[]
    friend_list_2=[]
    for friend in friend_list:
        friendname=friend.username
        friend_img=friend.img
        # friend_id=friend.id
        lastmessage=Talkroom.objects.all().filter(Q(you=request.user.id,friend=friend.id)|Q(you=friend.id,friend=request.user.id)).order_by("date").last()
        if lastmessage!=None:
            friend_list_1.append([friendname,lastmessage,friend_img,friend])
        else:
            friend_list_2.append([friendname,friend_img,friend])

    params={
        'friend_list_1':friend_list_1,
        'friend_list_2':friend_list_2,
    }
    return render(request, "myapp/friends.html",params)




def talk_room(request,num):
    friend = CustomUser.objects.get(id=num)
    message=Talkroom.objects.all().filter(Q(you=request.user.id,friend=friend.id)|Q(you=friend.id,friend=request.user.id)).order_by("date")
    params = {
        'username': friend,
        'form': TalkroomForm(),
        'message': message,
        'friend.id':friend.id
    }
    if (request.method == 'POST'):
        obj = Talkroom(you=request.user, friend=friend)
        form = TalkroomForm(request.POST, instance=obj)
        form.save()
        return render(request, "myapp/talk_room.html", params)
  
    return render(request, "myapp/talk_room.html",params)

def setting(request):
    return render(request, "myapp/setting.html")

def setting_name(request):
    id = CustomUser.objects.get(id=request.user.id)
    form = Setting_name(data=request.POST, instance=id)
    params={
            'form': form,
        }
    if(request.method == 'POST'):
        if form.is_valid():
            form.save()
            params={
                'message': 'Usernameの変更が完了しました。',
            }
            return render(request, "myapp/changeDone.html", params)
    return render(request, "myapp/settingName.html", params)


def setting_mail(request):
    id = CustomUser.objects.get(id=request.user.id)
    form = Setting_mail(data=request.POST, instance=id)
    params={
            'form': form,
        }
    if(request.method == 'POST'):
        if form.is_valid():
            form.save()
            params={
                'message': 'Emailの変更が完了しました。',
            }
            return render(request, "myapp/changeDone.html", params)
    return render(request, "myapp/settingMail.html", params)


def setting_img(request):
    id = CustomUser.objects.get(id=request.user.id)
    form = Setting_img(data=request.POST, instance=id)
    params={
            'form': form,
        }
    if(request.method == 'POST'):
        if form.is_valid():
            form.save()
            params={
                'message': 'Imgの変更が完了しました。',
            }
            return render(request, "myapp/changeDone.html", params)
    return render(request, "myapp/settingImg.html", params)

def setting_password(request):
    id = CustomUser.objects.get(id=request.user.id)
    form = Setting_password(data=request.POST, instance=id)
    params={
            'form': form,
        }
    if(request.method == 'POST'):
        if form.is_valid():
            form.save()
            params={
                'message': 'passwordの変更が完了しました。',
            }
            return render(request, "myapp/changeDone.html", params)
    return render(request, "myapp/settingPass.html", params)

