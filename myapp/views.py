from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Prefetch
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from operator import itemgetter
from .models import CustomUser, Message
from .forms import MessageForm, ChangeUsernameForm, ChangeEmailForm, ChangeImageForm, FriendSearchForm

class Index(TemplateView):
    template_name = "myapp/index.html"

class Friends(LoginRequiredMixin, TemplateView):
    template_name = "myapp/friends.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = FriendSearchForm()
        me = self.request.user
        filter = self.request.GET.get('filter') # 友だち検索機能
        
        if filter:
            otherusers = CustomUser.objects.filter(Q(username__icontains=filter) | Q(email__icontains=filter)).prefetch_related(
                Prefetch('user_from', queryset=Message.objects.filter(user_to=me).order_by('-time')),
                Prefetch('user_to', queryset=Message.objects.filter(user_from=me).order_by('-time'))
            )
            form.initial["filter"] = filter
        else:
            otherusers = CustomUser.objects.exclude(id=me.id).prefetch_related(
                Prefetch('user_from', queryset=Message.objects.filter(user_to=me).order_by('-time')),
                Prefetch('user_to', queryset=Message.objects.filter(user_from=me).order_by('-time'))
            )
            
        context['form'] = form
        friends = []
        for otheruser in otherusers:
            friend = {"user": otheruser}
            if otheruser.user_to.exists() or otheruser.user_from.exists():
                if otheruser.user_to.exists() and otheruser.user_from.exists():
                    sent = otheruser.user_to.first()
                    received = otheruser.user_from.first()
                    if sent.time < received.time:
                        recent_talk = received
                    else:
                        recent_talk = sent
                elif (not otheruser.user_to.exists()) and otheruser.user_from.exists():
                    recent_talk = otheruser.user_from.first()
                else:
                    recent_talk = otheruser.user_to.first()
                friend["date"] = recent_talk.time.astimezone(timezone.get_default_timezone())
                friend["message"] = recent_talk.message
            else:
                friend["date"] = otheruser.date_joined.astimezone(timezone.get_default_timezone())
            friend["view_date"] = get_view_date(friend["date"])
            friends.append(friend)
        context['friends'] = sorted(friends, key=itemgetter("date"), reverse=True)
        return context
    
def get_view_date(time): # 引数timeが，現在と同じ日なら時刻を，違う日なら日付を返す
    today = timezone.now().date()
    if time.date() == today:
        return str(time.hour) + ":" + str(time.minute).zfill(2)
    else:
        return str(time.month) + "/" + str(time.day)

class TalkRoom(LoginRequiredMixin, FormView):
    template_name = "myapp/talk_room.html"
    form_class = MessageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get("id") # Friend's id
        user = self.request.user
        friend = get_object_or_404(CustomUser, id=id)

        context["id"] = id
        context["friend"] = friend
        messages = (user.user_from.filter(user_to=friend) | user.user_to.filter(user_from=friend)).select_related("user_from").order_by("time")
        view_messages = [] # Templateに渡すためのview_messageを格納するリスト
        date = None # 以下のfor文で，メッセージを送信した日付が前のメッセージと異なるかどうかを判断する
        for message in messages:
            time = message.time.astimezone(timezone.get_default_timezone())
            view_message = {
                "user_from": message.user_from,
                "message": message.message,
                "date": time.date(),
                "time": str(time.hour) + ":" + str(time.minute).zfill(2),
                "viewdate_or_not": date != time.date(), # メッセージを送信した日付が変わるごとに日付を表示する
            }
            date = view_message["date"]
            view_messages.append(view_message)
        context["messages"] = view_messages
        return context

    def form_valid(self, form):
        if form.is_valid():
            Message.objects.create(
                user_from=self.request.user,
                user_to=CustomUser.objects.get(id=self.kwargs.get("id")),
                message=form.cleaned_data["message"]
            )
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("talk_room", kwargs={"id": self.kwargs.get("id")})

class SettingView(LoginRequiredMixin, TemplateView):
    template_name = "myapp/setting.html"

@login_required
def setting_username_view(request):
    if request.method == "POST":
        form = ChangeUsernameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, "myapp/setting_completed.html", {"content": "ユーザー名"})
    else:
        form = ChangeUsernameForm(instance=request.user)
    return render(request, "myapp/setting_username.html", {"form": form})

@login_required
def setting_email_view(request):
    if request.method == "POST":
        form = ChangeEmailForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, "myapp/setting_completed.html", {"content": "メールアドレス"})
    else:
        form = ChangeEmailForm(instance=request.user)
    return render(request, "myapp/setting_email.html", {"form": form})

@login_required
def setting_image_view(request):
    if request.method == "POST":
        currentimage = request.user.image
        form = ChangeImageForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            if form.cleaned_data.get("image") != currentimage: # 画像を選択しないまま送信して，画像が削除されてしまうのを防ぐ
                form.save(request.user)
            return render(request, "myapp/setting_completed.html", {"content": "プロフィール画像"})
    else:
        form = ChangeImageForm(instance=request.user)
    return render(request, "myapp/setting_image.html", {"form": form})

class SettingPassword(LoginRequiredMixin, PasswordChangeView):
    template_name = "myapp/setting_password.html"
    success_url = reverse_lazy("setting_password_done")
    
class SettingPasswordDone(PasswordChangeDoneView):
    template_name = "myapp/setting_completed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["content"] = "パスワード"
        return context
    
class LogoutDone(TemplateView):
    template_name = "myapp/logout_done.html"