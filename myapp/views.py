from django.contrib.auth import login
from .forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Prefetch, Q
from datetime import datetime, timezone

from .models import TalkRoom, Message

User = get_user_model()

def _normalize_pair(u1, u2):
    return (u1, u2) if u1.id < u2.id else (u2, u1)

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("friends")
    else:
        form = SignupForm()

    return render(request, "myapp/signup.html", {"form": form})



@transaction.atomic
def _get_or_create_dm_room(me, other):
    low, high = _normalize_pair(me, other)
    room, _ = TalkRoom.objects.get_or_create(user_low=low, user_high=high)
    return room


@login_required
def friends(request):
    me = request.user

    users = list(User.objects.exclude(id=me.id))

    rooms = (
        TalkRoom.objects
        .filter(Q(user_low=me) | Q(user_high=me))
        .select_related("user_low", "user_high")
        .prefetch_related(
            Prefetch(
                "messages",
                queryset=Message.objects.select_related("sender").order_by("-created_at"),
                to_attr="messages_desc",
            )
        )
    )

    room_info_by_other_id = {}
    for room in rooms:
        other = room.user_high if room.user_low_id == me.id else room.user_low
        last_msg = room.messages_desc[0] if room.messages_desc else None
        room_info_by_other_id[other.id] = (room, last_msg)

    items = []
    for u in users:
        room, last_msg = room_info_by_other_id.get(u.id, (None, None))
        items.append({
            "other": u,
            "room": room,
            "last_msg": last_msg,
        })

    items.sort(
    key=lambda x: (
        x["last_msg"] is not None, 
        x["last_msg"].created_at if x["last_msg"] else datetime.min.replace(tzinfo=timezone.utc),
    ),
    reverse=True
)

    return render(request, "myapp/friends.html", {"items": items})
    
@login_required
def start_dm(request, user_id):
    other = get_object_or_404(User, id=user_id)
    room = _get_or_create_dm_room(request.user, other)
    return redirect("talk_room", room_id=room.id)


@login_required
def talk_room(request, room_id):
    room = get_object_or_404(TalkRoom, id=room_id)

    if request.user.id not in (room.user_low_id, room.user_high_id):
        return redirect("friends")

    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        if text:
            Message.objects.create(room=room, sender=request.user, text=text)
        return redirect("talk_room", room_id=room.id)

    messages = room.messages.select_related("sender").order_by("created_at")
    other = room.user_high if room.user_low_id == request.user.id else room.user_low

    return render(
        request,
        "myapp/talk_room.html",
        {"room": room, "messages": messages, "other": other},
    )

def setting(request):
    return render(request, "myapp/setting.html")
