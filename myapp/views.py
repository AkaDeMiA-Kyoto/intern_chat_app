from genericpath import exists
from multiprocessing.sharedctypes import Value
from django.dispatch import receiver
from django.shortcuts import redirect, render
from .forms import SearchForm, SignUpForm, LoginForm, MessageForm,ProfImageForm,UserNameForm
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView,PasswordChangeDoneView
from django.urls import reverse_lazy
from .models import CustomUser,CustomMessage
from django.utils import timezone
from django.db.models import Q,Case,When,F,Exists
import datetime

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    form=SignUpForm()
    if request.method == 'POST':
        form=SignUpForm(request.POST, request.FILES, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            print("Form is not Valid!")
            for err in form.errors:
                print(err)
            return render(request, "myapp/signup.html",{'form':form})
        
    return render(request, "myapp/signup.html",{'form':form})

    

def friends(request):
    data=CustomUser.objects.all()
    form = SearchForm(request.POST)
    hasFormContent=False
    if (request.method=='POST' and request.POST['content']!=""):
        if "btn_reset" in request.POST:
            #フォームクリアボタンの処理。
            form = SearchForm()
        elif request.POST['content']!="":
            #検索処理
            searchName=request.POST['content']
            hasFormContent=True
            data=data.filter(username__contains=searchName)
    
    #最新メッセージの日時でソート
    #myMsg=CustomMessage.objects.filter(Q(primeUser=request.user)).order_by(F('createdTime'))
    myMsg=request.user.msg.all().order_by(F('createdTime'))
    #print(myMsg.count())
    friends=[]
    for friend in data:
        #直近のメッセージ取得
        lastMsg=myMsg.filter(Q(subUser=friend)).last()

        #画像URL、なければ置き換え
        prof_img_url="myapp/img/nullImage"
        if (friend.prof_img):
            print(friend.prof_img)
            prof_img_url=friend.prof_img.url
        
        if lastMsg!=None:
            print(friend.username+' had no msg with the user')
            friends.append({'id':friend.id,'username':friend.username,
            'prof_img_url':prof_img_url,'order':lastMsg.createdTime})
        else:
            print(friend.username)
            friends.append({'id':friend.id,'username':friend.username,
            'prof_img_url':prof_img_url,
            'order':friend.date_joined+datetime.timedelta(weeks=-20000)})
    friends.sort(key=lambda x: x['order'],reverse=True)
    
    hasData= data.count() > 0
    params={
        'form':form,
        'hasData':hasData,
        'data':friends,
        'hasFormContent':hasFormContent,
    }
    return render(request, "myapp/friends.html",params)

def talk_room(request,talkee):
    #存在しないIDのページにアクセスした場合
    if(CustomUser.objects.filter(id=talkee).last()==None):
        return render(request, "myapp/talk_room.html",{'isValidUrl':False})

    #フォーム、ID、画像登録
    mform=MessageForm()
    myImg="myapp/img/nullImage"
    if(request.user.prof_img):
        myImg=request.user.prof_img.url
    #if (CustomUser.objects.get(id=myid).prof_img):
    #    myImg=CustomUser.objects.get(id=myid).prof_img.url
    theirImg="myapp/img/nullImage"
    them=CustomUser.objects.get(id=talkee)
    if (them.prof_img):
        theirImg=them.prof_img.url

    #メッセージ送信
    if request.method == 'POST':
        msgTime=timezone.now().isoformat()
        msgContent=request.POST['content']
        msg=CustomMessage(content=msgContent,
        primeUser=request.user,subUser=them,
        isReceipt=False,createdTime=msgTime)
        msg.save()
        dummyMsg=CustomMessage(content=msgContent,
        primeUser=them,subUser=request.user,
        isReceipt=True,createdTime=msgTime)
        dummyMsg.save()
    
    #メッセージ取得、ソート
    #msgraw=CustomMessage.objects.filter(Q(primeUser=request.user)).order_by("createdTime")
    msgraw=request.user.msg.all()

    #表示
    dic={
        'isValidUrl':True,
        'self':talkee,
        'name':them.username,
        'form':mform,
        'msg':msgraw,
        'myImg':myImg,
        'theirImg':theirImg
    }
    return render(request, "myapp/talk_room.html",dic)

def setting(request):
    return render(request, "myapp/setting.html")

def changeUserName(request):
    form=UserNameForm(request.POST)
    err = ""
    if(request.method=='POST'):
        if(form.is_valid() or request.POST['username'] == request.user.username):
            form=UserNameForm(request.POST,instance=request.user)
            form.save()
            return redirect('setting')
        else :
            err=form.errors
    dic={
        'title':'Change User Name',
        'form':form,
        'err':err
    }
    return render(request,"myapp/simpleform.html",dic)

def changeProfImg(request):
    form=ProfImageForm(request.FILES)
    err = ""
    if(request.method=='POST'):
        if (form.is_valid):
            form=ProfImageForm(request.POST,request.FILES,instance=request.user)
            form.save()
            return redirect('setting')
        else :
            form=ProfImageForm(request.FILES)
            err=form.errors
            
    dic={
        'title':'Change Profile Image',
        'form':form,
        'err':err
    }
    return render(request,"myapp/simpleform.html",dic)

class MyLoginView(LoginView):
    authentication_form=LoginForm
    template_name="myapp/login.html"

class Logout(LogoutView):
    template_name='myapp/logout.html'