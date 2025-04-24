from django.shortcuts import redirect, render, get_object_or_404
from .forms import (
    SignUpForm,
    LoginForm,
    ChatMessageForm,
    ChangeNameForm,
    ChangeMailForm,
    ChangeIconForm,
)
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from django.views import View
from .models import CustomUser, TalkLog
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth import logout
from django.views import generic
from django.urls import reverse_lazy
from django.db.models import OuterRef, Subquery
from django.db.models import F
from django.db.models import Prefetch


def index(request):
    return render(request, "myapp/index.html")


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("myapp:index")
        return render(request, "myapp/signup.html", {"form": form})
    elif request.method == "GET":
        form = SignUpForm()
        return render(request, "myapp/signup.html", {"form": form})


class Login_View_Class(LoginView):
    template_name = "myapp/login.html"
    form_class = LoginForm


login_view = Login_View_Class.as_view()


class FriendsView(LoginRequiredMixin, View):
    def get(self, request):
        latest_log = TalkLog.objects.filter(
            Q(fromuser=OuterRef("pk"), touser=request.user)
            | Q(touser=OuterRef("pk"), fromuser=request.user)
        ).order_by("-timestamp")

        users = CustomUser.objects.annotate(
            latest_message=Subquery(latest_log.values("message")[:1]),
            latest_timestamp=Subquery(latest_log.values("timestamp")[:1]),
        )

        return render(request, "myapp/friends.html", {"users": users})


friends_view = FriendsView.as_view()


class TalkRoomView(LoginRequiredMixin, View):
    def get(self, request, id):
        touser = get_object_or_404(CustomUser, id=id)
        form = ChatMessageForm()

        talklog = (
            TalkLog.objects.select_related("fromuser")
            .filter(
                Q(touser=id, fromuser=request.user.id)
                | Q(touser=request.user.id, fromuser=id)
            )
            .order_by("timestamp")
        )

        return render(
            request,
            "myapp/talk_room.html",
            {"To_user": touser, "form": form, "talklog": talklog},
        )

    def post(self, request, id):
        form = ChatMessageForm(request.POST)
        touser = get_object_or_404(CustomUser, id=id)
        if form.is_valid():
            TalkLog.objects.create(
                message=form.cleaned_data["message"],
                touser=touser,
                fromuser=request.user,
            )
            return redirect(request.path)
        else:
            return render(
                request, "myapp/talk_room.html", {"To_user": touser, "form": form}
            )


talk_room = TalkRoomView.as_view()


class SettingView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "myapp/setting.html")


setting_view = SettingView.as_view()


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("myapp:index")


logout_view = LogoutView.as_view()


class ChangeNameView(LoginRequiredMixin, View):
    def get(self, request):
        form = ChangeNameForm()
        return render(request, "myapp/change_name.html", {"form": form})

    def post(self, request):
        form = ChangeNameForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.get(id=request.user.id)
            user.username = form.cleaned_data["username"]
            user.save()
            changed_field = "ユーザーネーム"
            return render(
                request, "myapp/change_done.html", {"changed_field": changed_field}
            )
        else:
            return redirect(request.path)


class ChangeMailView(LoginRequiredMixin, View):
    def get(self, request):
        form = ChangeMailForm()
        return render(request, "myapp/change_mail.html", {"form": form})

    def post(self, request):
        form = ChangeMailForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.get(id=request.user.id)
            user.email = form.cleaned_data["email"]
            user.save()
            changed_field = "メールアドレス"
            return render(
                request, "myapp/change_done.html", {"changed_field": changed_field}
            )
        else:
            return redirect(request.path)


class ChangeIconView(LoginRequiredMixin, View):
    def get(self, request):
        form = ChangeIconForm()
        return render(request, "myapp/change_icon.html", {"form": form})

    def post(self, request):
        form = ChangeIconForm(request.POST, request.FILES)
        if form.is_valid():
            user = CustomUser.objects.get(id=request.user.id)
            user.image = form.cleaned_data["image"]
            user.save()
            changed_field = "アイコン"
            return render(
                request, "myapp/change_done.html", {"changed_field": changed_field}
            )
        else:
            return redirect(request.path)
