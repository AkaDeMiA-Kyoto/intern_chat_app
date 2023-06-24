from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, LogoutView
from .forms import CustomSignupForm, MessageForm, ChangeUsernameForm, ChangeEmailForm, ChangeImageForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Message
import pytz
from datetime import datetime
from operator import attrgetter
from django.views.generic.edit import FormView

def index(request):
    return render(request, "myapp/index.html")

class Friends(LoginRequiredMixin, TemplateView):
    template_name = "myapp/friends.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        otherusers = CustomUser.objects.exclude(username=self.request.user.username)
        friends = []
        for otheruser in otherusers:
            friend = Friend(otheruser.username, otheruser.id, otheruser.image)
            recent_talks = (Message.objects.filter(user_from=self.request.user.id, user_to=friend.id) | Message.objects.filter(user_from=friend.id, user_to=self.request.user.id))
            if recent_talks:
                recent_talk = recent_talks.latest("time")
                friend.date = recent_talk.time.astimezone(pytz.timezone('Asia/Tokyo'))
                friend.message = recent_talk.message
            else:
                friend.date = otheruser.date_joined.astimezone(pytz.timezone('Asia/Tokyo'))
                friend.message = "You have not talked yet."
            friend.view_date = get_view_date(friend.date)
            friends.append(friend)
        context['friends'] = sorted(friends, key=attrgetter("date"), reverse=True)
        return context

class TalkRoom(LoginRequiredMixin, FormView):
    template_name = "myapp/talk_room.html"
    form_class = MessageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get("id")
        friend = get_object_or_404(CustomUser, id=id)
        context["id"] = id
        context["friendname"] = friend.username
        messages = (Message.objects.filter(user_from=self.request.user.id, user_to=id) | Message.objects.filter(user_from=id, user_to=self.request.user.id)).order_by("time")
        view_messages = [] # Templateに渡すためのViewMessageオブジェクトを格納するリスト
        date = None # メッセージを送信した日付が，前のメッセージと異なるかどうかを判断する
        for message in messages:
            if message.user_from == self.request.user.id:
                is_message_mine = True
            else:
                is_message_mine = False
            view_message = ViewMessage(message, is_message_mine)
            if date == view_message.date:
                view_message.viewdate_or_not = False
            else:
                view_message.viewdate_or_not = True
            date = view_message.date
            view_messages.append(view_message)
        context["messages"] = view_messages
        context["myimage"] = self.request.user.image
        context["yourimage"] = friend.image
        return context
    
    def form_valid(self, form):
        if form.is_valid():
            Message.objects.create(
                user_from=self.request.user.id,
                user_to=self.kwargs.get("id"),
                message=form.cleaned_data["message"]
            )
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("talk_room", kwargs={"id": self.kwargs.get("id")})

@login_required
def setting_view(request):
    return render(request, "myapp/setting.html")

@login_required
def setting_username_view(request):
    if request.method == "POST":
        form = ChangeUsernameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, "myapp/setting_username.html", {"completed": True})
    else:
        form = ChangeUsernameForm(instance=request.user)
    return render(request, "myapp/setting_username.html", {"form": form})

@login_required
def setting_email_view(request):
    if request.method == "POST":
        form = ChangeEmailForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, "myapp/setting_email.html", {"completed": True})
    else:
        form = ChangeEmailForm(instance=request.user)
    return render(request, "myapp/setting_email.html", {"form": form})

@login_required
def setting_image_view(request):
    currentimage = str(request.user.image)
    if request.method == "POST":
        form = ChangeImageForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            if str(form.cleaned_data.get("image")) != currentimage: # 画像を選択しないまま送信して，画像が削除されてしまうのを防ぐ
                form.save(request.user)
            return render(request, "myapp/setting_image.html", {"completed": True, "currentimage": form.cleaned_data.get("image")})
    else:
        form = ChangeImageForm(instance=request.user)
    return render(request, "myapp/setting_image.html", {"form": form, "currentimage": currentimage})

class SettingPassword(LoginRequiredMixin, PasswordChangeView):
    template_name = "myapp/setting_password.html"
    success_url = reverse_lazy("setting_password_done")
    
class SettingPasswordDone(PasswordChangeDoneView):
    template_name = "myapp/setting_password.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["completed"] = True
        return context

def logout(request):
    return render(request, "myapp/logout.html")

class Friend:
    def __init__(self, username, id, image):
        self.username = username
        self.id = id
        self.image = image

class ViewMessage: # トークルームで表示するメッセージをTemplateに渡すためのクラス
    def __init__(self, message, is_message_mine):
        self.message = message.message
        messagetime = message.time.astimezone(pytz.timezone('Asia/Tokyo'))
        self.date = messagetime.date()
        self.username = CustomUser.objects.get(id=message.user_from).username
        if messagetime.minute < 10:
            self.time = str(messagetime.hour) + ":0" + str(messagetime.minute)
        else:
            self.time = str(messagetime.hour) + ":" + str(messagetime.minute)
        self.is_message_mine = is_message_mine

def get_view_date(time): # 引数timeが，現在と同じ日なら時刻を，違う日なら日付を返す
    timezone = pytz.timezone('Asia/Tokyo')
    today = datetime.now().astimezone(timezone).date()
    if time.date() == today:
        if time.minute < 10:
            return str(time.hour) + ":0" + str(time.minute)
        else:
            return str(time.hour) + ":" + str(time.minute)
    else:
        return str(time.month) + "/" + str(time.day)