from os import error, name
from django import forms
from django.core.checks import messages
from django.db.models.query_utils import Q
from django.forms.fields import CharField
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import LoginForm, NameAlterForm,MailAlterForm, PassAlterForm, ImageAlterForm, SendForm, SignupForm
from .models import Message, Talker
from django.db.models import QuerySet
from django.core.exceptions import ImproperlyConfigured, ValidationError
import datetime





class Preserver():
    LoggedIn_ID = 0
pres = Preserver()


    #nameがuniqueであることを利用して、名前からtalkerを探すメソッド
    #存在しなければNoneを返す
def findByName(Name=''):
    data = Talker.objects.filter(name=Name)
    if data.exists:
        for d in data:
            return d
    else:
        return None
    

def findByID(ID=0):
    data = Talker.objects.filter(id=ID)
    if data.exists:
        for d in data:
            return d
    else:
        return None
    


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    params = {
        'title':'会員登録',
            'msg':'',
        'form':SignupForm(),
    }
    if(request.method == 'POST'):
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            name = request.POST['username']
            mail = request.POST['mail']
            password = request.POST['password1']
            img = request.FILES['image']
            talker = Talker(name=name, mail=mail, password = password, image = img)
            try:
                talker.validate_unique()
                talker.save()
                return redirect(to='/')

            except ValidationError:
                params = {
                'title':'会員登録',
                'msg':'既にこの名前は使われています',
                'form':SignupForm(request.POST, request.FILES),
                }
                return render(request, "myapp/signup.html", params)

        else:
            params = {
                'title':'会員登録',
                'msg':'入力内容に不備があります',
                'form':SignupForm(request.POST, request.FILES),
                }
    return render(request, "myapp/signup.html", params)

def login_view(request):
    params = {
        'msg':'',
        'form':LoginForm(),
    }
    if(request.method == 'POST'):
        talker = findByName(request.POST['name'])
        if(talker == None):
            params = {
                'msg':'ユーザーネームが間違っています',
                'form':LoginForm(request.POST),
                }
        else:
            if(request.POST['password'] == talker.password):
                pres.LoggedIn_ID =  talker.id
                return redirect(to='/friends')
            else:
                params = {
                    'msg':'パスワードが間違っています',
                    'form':LoginForm(request.POST),
                    }   
    return render(request, "myapp/login.html", params)

def latestMsgContent(counterpart, user):
    messages = Message.objects.filter(Q(sender = user,recipient = counterpart)|Q(sender = counterpart,recipient = user)).order_by('time').reverse()
    if(messages.count() == 0):
        return ""
    else:
        for msg in messages:
            return msg.content
    
def latestMsgTime(counterpart, user):
    messages = Message.objects.filter(Q(sender = user,recipient = counterpart)|Q(sender = counterpart,recipient = user)).order_by('time').reverse()
    if(messages.count() == 0):
        return ""
    else:
        for msg in messages:
            y = str(msg.time.year)
            m = str(msg.time.month)
            d = str(msg.time.day)
            h = str(msg.time.hour)
            min = str(msg.time.minute)
            return y + "-" + m + "-" + d + " " + h + ":" + min

def friends(request):
    user = findByID(pres.LoggedIn_ID)
    if (user == None):
        return redirect(to='logout_view')
    
    messages = Message.objects.filter(Q(sender = user)|Q(recipient = user)).order_by('time').reverse()
    friendsList = []
    data = []

    for msg in messages:
        if(msg.sender == user):
            friendsList.append(msg.recipient)
        else:
            friendsList.append(msg.sender)
    for friend in Talker.objects.all().order_by('time'):
        friendsList.append(friend)
    friendsList = list(dict.fromkeys(friendsList))
    friendsList.remove(findByID(pres.LoggedIn_ID))
    for friend in friendsList:
        data.append([friend,latestMsgContent(friend, user),latestMsgTime(friend, user)])

    params = {
        'data': data ,
    }
    return render(request, "myapp/friends.html", params)

def talk_room(request,id):
    sndr = findByID(pres.LoggedIn_ID)
    rcpt = findByID(id)
    if(sndr == None):
        return redirect(to='logout_view')
    
    if(request.method == 'POST'):
        cnt = request.POST['content']
        Message(content = cnt, sender = sndr, recipient = rcpt).save()

    msglist = Message.objects.filter(Q(sender = sndr,recipient = rcpt)|Q(sender = rcpt,recipient = sndr)).order_by('time')
    data = []
    for msg in msglist:
        y = str(msg.time.year)
        m = str(msg.time.month)
        d = str(msg.time.day)
        h = str(msg.time.hour)
        min = str(msg.time.minute)
        if int(min)<10:
            min = "0"+ min
        date = y + "-" + m + "-" + d + " " + h + ":" + min
        data.append([msg,date])
    params = {
        'id':id,
        'msglist':data,
        'name':rcpt.name,
        'form':SendForm(),
        }
    return render(request, "myapp/talk_room.html", params)

def setting(request):
    return render(request, "myapp/setting.html", {'title':'設定'})

def name_altering(request):
    obj = findByID(pres.LoggedIn_ID)
    if (findByID(pres.LoggedIn_ID) == None):
        return render(request, "myapp/logout.html", {'msg':'ログインできていません'})
    if(request.method =='POST'):
        obj.name = request.POST['newVal']
        try:
            obj.validate_unique()
            obj.save()
            params ={
            'title':'ユーザーネームの変更',
            'msg':'ユーザーネーム変更完了',
            'form': '',
            }
            return render(request, "myapp/alter.html", params)
        except ValidationError:
            params = {
                'title':'ユーザーネームの変更',
                'msg':'既にこの名前は使われています',
                'form':NameAlterForm(request.POST),
                }
            return render(request, "myapp/alter.html", params)
    params ={
        'title':'ユーザーネームの変更',
        'msg':'',
        'form': NameAlterForm()
    }
    return render(request, "myapp/alter.html", params)

def mail_altering(request):
    obj = findByID(pres.LoggedIn_ID)
    if (findByID(pres.LoggedIn_ID) == None):
        return render(request, "myapp/logout.html", {'msg':'ログインできていません'})
    if(request.method=='POST'):
        obj.mail = request.POST['newVal']
        obj.save()
        params ={
            'title':'メールアドレスの変更',
            'msg':'メールアドレス変更完了',
            'form': '',
            }
        return render(request, "myapp/alter.html", params)
    params ={
        'title':'メールアドレスの変更',
        'msg':'',
        'form': MailAlterForm()
    }
    return render(request, "myapp/alter.html", params)
    
def pass_altering(request):
    obj = findByID(pres.LoggedIn_ID)
    if (findByID(pres.LoggedIn_ID) == None):
        return render(request, "myapp/logout.html", {'msg':'ログインできていません'})
    
    params ={
        'title':'パスワードの変更',
        'msg':'',
        'form': PassAlterForm()
    }
    if(request.method=='POST'):
        form = PassAlterForm(request.POST)
        if (request.POST['password1'] != request.POST['password2']):
            params ={
            'title':'パスワードの変更',
            'msg':'確認用パスワードが一致しません',
            'form': PassAlterForm(),
                }
        else: 
            obj.save()
            params ={
            'title':'パスワードの変更',
            'msg':'パスワード変更完了',
            'form': '',
                }        
    return render(request, "myapp/alter.html", params)

def image_altering(request):
    obj = findByID(pres.LoggedIn_ID)
    if (findByID(pres.LoggedIn_ID) == None):
        return render(request, "myapp/logout.html", {'msg':'ログインできていません'})
    if(request.method=='POST'):
        obj.image = request.FILES['newVal']
        obj.save()
        params ={
            'title':'アイコンの変更',
            'msg':'アイコン変更完了',
            'form': '',
            }
        return render(request, "myapp/alter.html", params)
    params ={
        'title':'アイコンの変更',
        'msg':'',
        'form': ImageAlterForm()
    }
    return render(request, "myapp/alter.html", params)

def logout_view(request):
    pres.LoggedIn_ID = 0
    return render(request, "myapp/logout.html", {'msg':'ログアウトしました'})