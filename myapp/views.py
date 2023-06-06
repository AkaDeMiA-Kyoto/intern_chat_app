from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from .forms import SignUpForm, MessageForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser, Message
import pytz
from .functions import get_view_date
from operator import attrgetter
from django.views.generic.edit import FormView

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("index")
    else:
        form = SignUpForm()
    return render(request, "myapp/signup.html", {"form": form})

class Login(LoginView):
    template_name = "myapp/login.html"

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
        context["slug"] = self.kwargs.get("slug")
        id = CustomUser.objects.get(username=self.kwargs.get("slug")).id
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
        context["yourimage"] = CustomUser.objects.get(id=id).image
        return context
    
    def form_valid(self, form):
        if form.is_valid():
            Message.objects.create(
                user_from=self.request.user.id,
                user_to=CustomUser.objects.get(username=self.kwargs.get("slug")).id,
                message=form.cleaned_data["message"]
            )
        TalkRoom.success_url = "/talk_room/" + self.kwargs.get("slug")
        return super().form_valid(form)

class Setting(LoginRequiredMixin, TemplateView):
    template_name = "myapp/setting.html"

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