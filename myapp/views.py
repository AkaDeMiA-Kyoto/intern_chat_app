from django.shortcuts import redirect, render
from django.contrib.auth import login
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .models import CustomUser, Message
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request):
    return render(request, "myapp/index.html")


def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("index")
        else:
            return render(request, "myapp/signup.html", {"form": form})

    return render(request, "myapp/signup.html")


class CustomLoginView(LoginView):
    template_name = "myapp/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("friends")
    authentication_form = CustomAuthenticationForm

    def get_success_url(self):
        return self.success_url


@login_required
def friends(request):
    users = CustomUser.objects.exclude(id=request.user.id)
    current_user = request.user

    message_users = []
    for user in users:
        received_message = user.received_messages.filter(send_by=current_user).last()
        sent_message = user.sent_messages.filter(send_to=current_user).last()
        latest_message = None

        if received_message or sent_message:
            if received_message:
                latest_message = received_message
            elif sent_message:
                latest_message = sent_message
            else:
                if received_message.created_at < sent_message.created_at:
                    latest_message = sent_message
                else:
                    latest_message = received_message

        message_users.append({"user": user, "latest_message": latest_message})

    sorted_users = sorted(
        message_users,
        key=lambda entry: (
            0 if entry["latest_message"] else 1,
            (
                -entry["latest_message"].created_at.timestamp()
                if entry["latest_message"]
                else -entry["user"].date_joined.timestamp()
            ),
        ),
        reverse=False,
    )

    return render(request, "myapp/friends.html", {"user_objects": sorted_users})


@login_required
def talk_room(request, user_id):
    if request.method == "GET":
        recieved_user = CustomUser.objects.get(id=user_id)
        current_user = request.user
        messages = Message.objects.filter(
            (Q(send_by=current_user) | Q(send_by=recieved_user))
            & (Q(send_to=recieved_user) | Q(send_to=current_user))
        ).order_by("created_at")

        return render(
            request,
            "myapp/talk_room.html",
            {"recieved_user": recieved_user, "messages": messages},
        )

    elif request.method == "POST":
        recieved_user = CustomUser.objects.get(id=user_id)
        current_user = request.user
        content = request.POST.get("content")

        Message.objects.create(
            content=content,
            created_at=datetime.now(),
            send_to=recieved_user,
            send_by=current_user,
        )

        return redirect("talk_room", user_id=recieved_user.id)


@login_required
def setting(request):

    return render(request, "myapp/setting.html")
