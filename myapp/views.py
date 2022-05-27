from django.contrib import auth
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic

from .forms import SignUpForm, LoginForm, TalkForm, UsernameChangeForm, EmailChangeForm
from .models import User, Talk

class IndexView(generic.TemplateView):
    template_name = "myapp/index.html"


def signup_view(request):
    form = None
    if request.method == "GET":
        form = SignUpForm()
    elif request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]

            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)
            return redirect("index")
    context = {"form": form}
    return render(request, "myapp/signup.html", context)

class LoginView(auth_views.LoginView):
    authentication_form = LoginForm
    template_name = "myapp/login.html"

@login_required
def friends(request):
    friends = User.objects.exclude(id=request.user.id)
    context = {"friends": friends}
    print(friends)
    return render(request, "myapp/friends.html", context)

@login_required
def talk_room(request, user_id):
    form = None
    friend = get_object_or_404(User, id=user_id)

    talks = Talk.objects.filter(
        Q(sender=request.user, receiver=friend)
        |   Q(sender=friend, receiver=request.user)
    ).order_by("time")

    if request.method == "GET":
        form = TalkForm()
    elif request.method == "POST":
        form = TalkForm(request.POST)
        if form.is_valid():
            new_talk = form.save(commit=False)
            new_talk.sender = request.user
            new_talk.receiver = friend
            new_talk.save()
            return redirect("talk_room", user_id)
    context = {
        "form": form,
        "friend": friend,
        "talks": talks,
    }
    return render(request, "myapp/talk_room.html", context)

def setting(request):
    return render(request, "myapp/setting.html")

@login_required
def setting_username(request):
    form = None
    if request.method == "GET":
        form = UsernameChangeForm(instance=request.user)
    elif request.method == "POST":
        form = UsernameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("setting_username_completed")
    
    context = {"form": form}
    return render(request, "myapp/setting_username.html", context)

@login_required
def setting_mailaddress(request):
    if request.method == "GET":
        form = EmailChangeForm(instance=request.user)
    elif request.method == "POST":
        form = EmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("setting_mailaddress_completed")
    
    context = {"form": form}
    return render(request, "myapp/setting_mailaddress.html", context)

@login_required
def setting_icon(request):
    return render(request, "myapp/setting_icon.html")

class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = "myapp/setting_password.html"
    success_url = reverse_lazy("setting_password_completed")

class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = "myapp/setting_password_completed.html"

@login_required
def setting_username_completed(request):
    return render(request, "myapp/setting_username_completed.html")

@login_required
def setting_mailaddress_completed(request):
    return render(request, "myapp/setting_mailaddress_completed.html")

@login_required
def setting_icon_completed(request):
    return render(request, "myapp/setting_icon_completed.html")

class LogoutView(auth_views.LogoutView):
    pass
