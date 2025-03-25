from django.shortcuts import redirect,get_object_or_404, render
from django.contrib.auth import login
from .forms import SingupForm, LoginForm, MessageSend
from django.contrib.auth.decorators import login_required
from .models import Signup, Message


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    form = SingupForm()
    if request.method == "GET": 
        return render(request, "myapp/signup.html", {'form' : form})
    if request.method == "POST":
        form = SingupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("myapp:index")
    return render(request,"myapp/signup.html", {'form' : form})

def login_view(request):
    form = LoginForm()
    if request.method == "GET":
        return render(request, "myapp/login.html", {'form' : form})
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("myapp:friends")
    return render(request, "myapp/login.html", {'form' : form})

@login_required
def friends(request):
    users = Signup.objects.exclude(id=request.user.id)
    return render(request, "myapp/friends.html", {'users': users})

@login_required
def talk_room(request,user_id):
    form = MessageSend()
    #ユーザー間でトークルームが重複しないための処理
    myself_id = request.user.id
    if myself_id > user_id:
        user1 = user_id
        user2 = myself_id
    else:
        user1 = myself_id
        user2 = user_id
    myself = request.user
    user = get_object_or_404(Signup, id = user_id) #送信相手
    if request.method == "GET":
        #メッセージを送信順に表示する
        messages = Message.objects.filter(user1 = user1, user2 = user2).order_by('-sended_at')
        return render(request, "myapp/talk_room.html", {'myself':myself, 'user':user, 'messages':messages, 'form':form})

    if request.method == "POST":
        form = MessageSend(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = user
            message.user1 = user1
            message.user2 = user2
            message.save()
            return redirect("myapp:talk_room", user_id = user_id)
        

@login_required
def setting(request):
    return render(request, "myapp/setting.html")

