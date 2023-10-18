from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from .forms import SignupForm, CustomAuthenticationForm, MessageForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Message
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == "GET":
        form = SignupForm()
        return render(request, "myapp/signup.html", {"form": form}) #formを描画
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES) #POSTデータをformに保存
        if form.is_valid():
            form.save()
            return render(request, "myapp/index.html")
        else:
            form = SignupForm(request.POST, request.FILES)
            return render(request, "myapp/signup.html", {"form": form})


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm

def login_view(request):
    return CustomLoginView.as_view(template_name="myapp/login.html")(request)

@login_required
def friends(request):
    friend_list = []
    for friend in CustomUser.objects.all():
        if friend.id != request.user.id:    #自身を除く
            friend_list.append(friend)
    temp_friend_info = []
    time_list = []
    nontalk_friend_list = []
    id_list = []
    for friend in friend_list:
        talk_log = []
        for past_message in Message.objects.all():            #フレンドごとにトーク履歴を取得
            if past_message.sender == request.user.id and past_message.receiver == friend.id:
                talk_context = past_message.message
                time = past_message.time
                talk_log.append(past_message)
            if past_message.sender == friend.id and past_message.receiver == request.user.id:
                talk_context = past_message.message
                time = past_message.time
                talk_log.append(past_message)
        if talk_log:    #リストが空かどうかの判定
            latest_message = talk_log[0]    #フレンドごとに最新のトークを取得
            for message in talk_log:
                if latest_message.time < message.time:
                    latest_message = message
            time_list.append(latest_message.time)       #最新のトーク時間を記録
            friend_dict = {"friend_id":friend.id, "friend_name":friend.username, "friend_image":friend.image, "latest_message":latest_message.message, "time":latest_message.time}
            temp_friend_info.append(friend_dict)    #フレンドの情報をまとめて辞書化、リストに格納
        else:   #トークしていない友達の処理
            nontalk_friend_list.append(friend)
            id_list.append(friend.id)
    friend_info = sorted(temp_friend_info, key=lambda x: x["time"], reverse=True)
    sorted(id_list, reverse=True)       #登録順にソート
    nontalk_friend_info = []
    for id in id_list:
        for friend in nontalk_friend_list:
            if friend.id == id:
                nontalk_friend_info.append({"friend_id":friend.id, "friend_name":friend.username, "friend_image":friend.image})     #登録順に並べる

    context = {
        "friend_info":friend_info,
        "nontalk_friend_info":nontalk_friend_info
    }
    return render(request, "myapp/friends.html", context)


@login_required
def talk_room(request, friend_id):
        my_id = request.user.id
        friend_name = CustomUser.objects.get(id=friend_id)
        context = {
           "friend_id" : friend_id,
           "friend_name" : friend_name
       }  
        initials = { 
            "sender" : request.user.id,
            "receiver" : friend_id,
        }
    
        if request.method == "GET":
            form = MessageForm(initial= initials)
            talk_log = []
            for past_message in Message.objects.all():            #トーク履歴を取得
                if past_message.sender == request.user.id and past_message.receiver == friend_id:
                    sender_name = (CustomUser.objects.get(id = past_message.sender)).username
                    talk_context = past_message.message
                    time = past_message.time
                    talk_log.append({"sender_name":sender_name, "talk_context":talk_context, "time":time})
                if past_message.sender == friend_id and past_message.receiver == request.user.id:
                    sender_name = (CustomUser.objects.get(id = past_message.sender)).username
                    talk_context = past_message.message
                    time = past_message.time
                    talk_log.append({"sender_name":sender_name, "talk_context":talk_context, "time":time})
            return render(request, "myapp/talk_room.html", {**context, "form": form, "talk_log":talk_log})
        message_list = Message.objects.all()
        if request.method == "POST":
            form = MessageForm(request.POST, initial = initials)
            if form.is_valid():
                form.save()
            talk_log = []
            for past_message in Message.objects.all():            #トーク履歴を取得
                if past_message.sender == request.user.id and past_message.receiver == friend_id:
                    sender_name = (CustomUser.objects.get(id = past_message.sender)).username
                    talk_context = past_message.message
                    time = past_message.time
                    talk_log.append({":sender_name":sender_name, "talk_context":talk_context, "time":time})
                if past_message.sender == friend_id and past_message.receiver == request.user.id:
                    sender_name = (CustomUser.objects.get(id = past_message.sender)).username
                    talk_context = past_message.message
                    time = past_message.time
                    talk_log.append({"sender_name":sender_name, "talk_context":talk_context, "time":time})
            return redirect("talk_room", friend_id)


@login_required
def setting(request):
    return render(request, "myapp/setting.html")


class logout(LoginRequiredMixin, LogoutView):
    template_name = "myapp/index.html"


class passwordchange(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy("myapp:password_change_done")
    template_name = "myapp/password.html"


@login_required
def username(request):
    if request.method == "GET":
        form = SignupForm()
        return render(request, "myapp/username.html", {"form": form}) #formを描画
    if request.method == "POST":
        old_data = CustomUser.objects.get(id=request.user.id)
        old_data.username = request.POST.get("username")
        old_data.save()
        return render(request, "myapp/username_change_done.html")
    
@login_required
def username_change_done(request):
    return render(request, "myapp/username_change_done.html")

@login_required
def email(request):
    if request.method == "GET":
        form = SignupForm()
        return render(request, "myapp/email.html", {"form": form}) #formを描画
    if request.method == "POST":
        old_data = CustomUser.objects.get(id=request.user.id)
        old_data.email = request.POST.get("email")
        old_data.save()
        return render(request, "myapp/email_change_done.html")

@login_required
def email_change_done(request):
    return render(request, "myapp/email_change_done.html")

@login_required
def image(request):
    old_data = CustomUser.objects.get(id=request.user.id)
    context = {
        "image":old_data.image
    }
    if request.method == "GET":
        form = SignupForm()
        return render(request, "myapp/image.html", {**context, "form": form})
    if request.method == "POST":
        old_data.image = request.FILES.get("image")
        old_data.save()
        return render(request, "myapp/image_change_done.html")

@login_required
def image_change_done(request):
    return render(request, "myapp/image_change_done.html")






