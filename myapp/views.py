from django.shortcuts import redirect, render
from .forms import (
    CustomSignupForm,
    UsernameChangeForm,
    EmailChangeForm,
    ImageChangeForm,
)
from django.views.generic import TemplateView
from allauth.account.views import SignupView
from .models import CustomUser, Message
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist


class IndexView(TemplateView):
    template_name = "myapp/index.html"


class CustomSignupView(SignupView):
    form_class = CustomSignupForm


@login_required
def friends(request):
    users = CustomUser.objects.exclude(id=request.user.id)
    current_user = request.user

    message_users = []
    for user in users:
        received_message = (
            user.received_messages.filter(send_by=current_user)
            .order_by("-created_at")
            .first()
        )
        sent_message = (
            user.sent_messages.filter(send_to=current_user)
            .order_by("-created_at")
            .first()
        )
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
    try:
        recieved_user = CustomUser.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return redirect("friends")

    if request.method == "GET":
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
    current_user = request.user

    return render(request, "myapp/setting.html", {"user": current_user})


@login_required
def change_username(request):
    current_user = request.user
    if request.method == "POST":
        form = UsernameChangeForm(request.POST, request.FILES)
        if form.is_valid():
            current_user.username = form.cleaned_data["username"]
            current_user.save()

            return redirect("setting")
        else:
            return render(request, "myapp/change_username.html", {"form": form})
    else:
        return render(request, "myapp/change_username.html", {"user": current_user})


@login_required
def change_email(request):
    current_user = request.user
    if request.method == "POST":
        form = EmailChangeForm(request.POST, request.FILES)
        if form.is_valid():
            current_user.email = form.cleaned_data["email"]
            current_user.save()
            return redirect("setting")
        else:
            return render(request, "myapp/change_email.html", {"form": form})
    else:
        return render(request, "myapp/change_email.html", {"user": current_user})


@login_required
def change_image(request):
    current_user = request.user
    if request.method == "POST":
        form = ImageChangeForm(request.POST, request.FILES)
        if form.is_valid():
            current_user.image = form.cleaned_data["image"]
            current_user.save()
            return redirect("setting")
        else:
            return render(
                request, "myapp/change_image.html", {"form": form, "user": current_user}
            )
    else:
        return render(request, "myapp/change_image.html", {"user": current_user})


@login_required
def delete_user(request):
    current_user = request.user
    current_user.delete()

    return redirect("index")
