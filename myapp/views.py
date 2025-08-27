from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone

from .forms import (
    EmailChangeForm,
    IconChangeForm,
    LoginForm,
    SignUpForm,
    UsernameChangeForm,
)
from .models import Message


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            print("is_valid")
            form.save()
            return redirect('myapp:index')
    else:
        form = SignUpForm()

    return render(request, 'myapp/signup.html', {'form': form})

class login_view(LoginView):
    template_name = 'myapp/login.html'
    form_class = LoginForm

User = get_user_model()

@login_required
def talk_room(request, username):
    other_user = get_object_or_404(User, username=username)
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by("timestamp")

    if request.method == "POST":
        content = (request.POST.get("content") or "" )
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )
        return redirect("talk_room", username=other_user.username)
    return render(request, "myapp/talk_room.html",{
        "other_user":other_user,
        "messages":messages
    })

@login_required
def friends(request):
    all_users = User.objects.exclude(id=request.user.id)
    conversations = []

    for other in all_users:
        last_message = (Message.objects.filter(
        Q(sender=request.user, receiver=other) | Q(receiver=request.user, sender=other)
    ).select_related("sender", "receiver").order_by("-timestamp").first())
    
        conversations.append({
        "other": other,
        "last_message": last_message
        })

    conversations.sort (
        key=lambda c:c["last_message"].timestamp if c["last_message"] else timezone.make_aware(datetime.min),
        reverse=True
    )
    return render(request, "myapp/friends.html", {
        "conversations": conversations
    })

    
def setting(request):
    return render(request, "myapp/setting.html")
@login_required
def username_change(request):
    if request.method == "POST":
        form = UsernameChangeForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect ("myapp:username_change_done")
    else:
        form = UsernameChangeForm(instance = request.user)
    return render(request, "myapp/username_change.html", {"form": form})
@login_required
def username_change_done(request):
    return render(request, "myapp/username_change_done.html")

@login_required
def email_change(request):
    if request.method == "POST":
        form = EmailChangeForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect ("myapp:email_change_done")
    else:
        form = EmailChangeForm(instance = request.user)
    return render(request, "myapp/email_change.html", {"form": form})
@login_required
def email_change_done(request):
    return render(request, "myapp/email_change_done.html")

@login_required
def icon_change(request):
    if request.method == "POST":
        form = IconChangeForm(request.POST, request.FILES, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect ("myapp:icon_change_done")
    else:
            form = IconChangeForm(instance = request.user)
    return render(request, "myapp/icon_change.html", {"form": form})

def icon_change_done(request):
    return render(request, "myapp/icon_change_done.html")

class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    template_name='myapp/password_change.html'
    success_url = reverse_lazy("myapp:password_change_done")

class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'myapp/index.html'

