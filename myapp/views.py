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
from django.core.exceptions import ValidationError






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
    


def __new_str__(self):
    result = ''
    for item in self:
        result += '<h2><tr><td>' + '<img src=\''+ item.image.url+\
            '\' width=\'100\' height=\'100\'\ >' +'</td><td>' +\
            '<a href=\'http://127.0.0.1:8000/talk_room/'+ str(item.id) + '\' >'\
                + item.name +'</a></td>' + '</tr></h2>'
    return result

def index(request):
    for t in Talker.objects.all():
        print(t.name + " : " + str(t.time) + ", ")
    return render(request, "myapp/index.html")

def signup_view(request):
    params = {
        'title':'会員登録',
            'msg':'',
        'form':SignupForm(),
    }
    if(request.method == 'POST'):
        if(request.POST['conf_pass'] == request.POST['password']):
            name = request.POST['name']
            mail = request.POST['mail']
            password = request.POST['password']
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
                'msg':'パスワードと確認用のパスワードが一致しません',
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
                'msg':'does not exist',
                'form':LoginForm(request.POST),
                }
        else:
            if(request.POST['password'] == talker.password):
                pres.LoggedIn_ID =  talker.id
                return redirect(to='/friends')
            else:
                params = {
                    'msg':'wrong password',
                    'form':LoginForm(request.POST),
                    }   
    return render(request, "myapp/login.html", params)

def latestMsg(counterpart, user):
    messages = Message.objects.filter(Q(sender = user,recipient = counterpart)|Q(sender = counterpart,recipient = user)).order_by('time').reverse()
    if(messages.count() == 0):
        return ""
    else:
        for msg in messages:
            return str(msg)

def friends(request):
    # QuerySet.__str__ = __new_str__
    user = findByID(pres.LoggedIn_ID)
    if (user == None):
        return redirect(to='logout_view')
    
    messages = Message.objects.filter(Q(sender = user)|Q(recipient = user)).order_by('time').reverse()
    lis1 = []
    lis2 = []
    for msg in messages:
        if(msg.sender == user):
            lis1.append(msg.recipient)
        else:
            lis1.append(msg.sender)
    for talker in Talker.objects.all().order_by('time'):
        lis1.append(talker)
    lis1 = list(dict.fromkeys(lis1))
    lis1.remove(findByID(pres.LoggedIn_ID))
    for f in lis1:
        lis2.append(latestMsg(f, user))
    l = []
    for int in range(0, len(lis1)):
        l.append([lis2[int],lis1[int]])
        
    params = {
        'data': l ,
        'lis1': lis1,
        'lis2': lis2,
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
    params = {
        'msg':'',
        'msglist':msglist,
        'name':rcpt.name,
        'form':SendForm(),
        }
    return render(request, "myapp/talk_room.html", params)

def setting(request):
    return render(request, "myapp/setting.html")

def name_altering(request):
    if(request.method =='POST'):
        obj = findByID(pres.LoggedIn_ID)
        if (findByID(pres.LoggedIn_ID) == None):
            return redirect(to='logout_view')
        obj.name = request.POST['newVal']
        obj.save()
        return redirect(to='setting')
    params ={
        'form': NameAlterForm()
    }
    return render(request, "myapp/alter.html", params)

def mail_altering(request):
    if(request.method=='POST'):
        obj = findByID(pres.LoggedIn_ID)
        if (findByID(pres.LoggedIn_ID) == None):
            return redirect(to='logout_view')        
        obj.mail = request.POST['newVal']
        obj.save()
        return redirect(to='setting')
    params ={
        'form': MailAlterForm()
    }
    return render(request, "myapp/alter.html", params)
    
def pass_altering(request):
    if(request.method=='POST'):
        obj = findByID(pres.LoggedIn_ID)
        if (findByID(pres.LoggedIn_ID) == None):
            return redirect(to='logout_view')
        obj.password = request.POST['newVal']
        obj.save()
        return redirect(to='setting')
    params ={
        'form': PassAlterForm()
    }
    return render(request, "myapp/alter.html", params)

def image_altering(request):
    if(request.method=='POST'):
        obj = findByID(pres.LoggedIn_ID)
        if (obj == None):
            return redirect(to='logout_view')
        obj.image = request.FILES['newVal']
        obj.save()
        return redirect(to='setting')
    params ={
        'form': ImageAlterForm()
    }
    return render(request, "myapp/alter.html", params)

def logout_view(request):
    pres.LoggedIn_ID = 0
    return render(request, "myapp/logout.html", {'msg':'you logged out'})