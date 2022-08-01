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
    if (request.method=='POST' and request.POST['content']!=""):
        searchName=request.POST['content']
        data=data.filter(username__contains=searchName)
    myid=request.user.id
    myMsg=CustomMessage.objects.filter(Q(sender=myid)|Q(receiver=myid)).order_by(F('createdTime'))
    print(myMsg.count())
    friends=[]
    for friend in data:
        lastMsg=myMsg.filter(Q(sender=friend.id)|Q(receiver=friend.id)).last()

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
    }
    return render(request, "myapp/friends.html",params)

def talk_room(request,talkee):
    if(CustomUser.objects.filter(id=talkee).last()==None):
        return render(request, "myapp/talk_room.html",{'isValidUrl':False})
    mform=MessageForm()
    pagetitle=CustomUser.objects.get(id=talkee)
    myid=request.user.id
    if request.method == 'POST':
        msg=CustomMessage(content=request.POST['content'],
        sender=request.user.id,receiver=talkee,
        createdTime=timezone.now().isoformat())
        msg.save()
    msgraw=CustomMessage.objects.filter(
        Q(sender=myid)|Q(receiver=myid)
    ).filter(
        Q(sender=talkee)|Q(receiver=talkee)
    ).order_by("createdTime")
    dic={
        'isValidUrl':True,
        'self':talkee,
        'name':pagetitle,
        'form':mform,
        'msg':msgraw,
        'myImg':CustomUser.objects.get(id=myid).prof_img.url,
        'theirImg':CustomUser.objects.get(id=talkee).prof_img.url
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