from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from .forms import (
    TalkForm, 
    ImageSettingForm, 
    FriendsSearchForm, 
    PasswordChangeForm, 
    UserNameSettingForm,
    )
from django.db.models import Q
from django.contrib.auth.views import (
    PasswordChangeDoneView,
    PasswordChangeView,
)
from django.urls import reverse_lazy
from .models import Talk

from django.db.models import OuterRef, Subquery

User = get_user_model()


def index(request):
    return render(request, "myapp/index.html")

@login_required
def friends(request):
    user = request.user
    
    latest_msg = Talk.objects.filter(
            Q(talk_from=OuterRef("pk"), talk_to=user)
        |Q(talk_from=user, talk_to=OuterRef("pk"))
        ).order_by("-time")

    friends = User.objects.exclude(id=user.id).annotate(latest_msg_talk=Subquery(latest_msg.values("talk")[:1]))

    form = FriendsSearchForm()

    if request.method == "GET" and "friends_search" in request.GET:
        form = FriendsSearchForm(request.GET)

        if form.is_valid():
            keyword = form.cleaned_data.get("keyword")
            if keyword:
                latest_msg = Talk.objects.filter(
                        Q(talk_from=OuterRef("pk"), talk_to=user)
                    |Q(talk_from=user, talk_to=OuterRef("pk"))
                     ).order_by("-time")
                
                friends = User.objects.filter(Q(username__icontains=keyword) | Q(email__icontains=keyword)).annotate(latest_msg_talk=Subquery(latest_msg.values("talk")[:1]))

                context = {
                    "form": form,
                    "is_searched": True,
                    "friends": friends,
                }
                return render(request, "myapp/friends.html", context)
            
    context = {
        "friends": friends,
        "form": form,
    }
    return render(request, "myapp/friends.html", context)        


@login_required
def talk_room(request, user_id):

    user = request.user
    friend = get_object_or_404(User, id=user_id)

    talk = Talk.objects.filter(
        Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend)
    ).order_by("time")

    form = TalkForm()
    context = {
        "form": form,
        "talk": talk,
        "friend": friend,
    }

    if request.method == "POST":
        new_talk = Talk(talk_from=user, talk_to=friend)
        form = TalkForm(request.POST, instance=new_talk)

        if form.is_valid():
               
            form.save()

            return redirect("talk_room", user_id)
            
        else:

            print(form.errors)

    return render(request, "myapp/talk_room.html", context)

@login_required
def setting(request):
    return render(request, "myapp/setting.html")

@login_required
def user_img_change(request):
    user = request.user
    if request.method == "GET":
        form = ImageSettingForm(instance=user)

    elif request.method == "POST":
        form = ImageSettingForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user_img_change_done")
        
        else:
             print(form.errors)

    context = {
        "form": form,
    }
    return render(request, "myapp/user_img_change.html", context)
    
@login_required
def user_img_change_done(request):
    return render(request, "myapp/user_img_change_done.html")

@login_required
def username_change(request):
    user = request.user
    if request.method == "GET":
        form = UserNameSettingForm(instance=user)

    elif request.method == "POST":
        form = UserNameSettingForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("username_change_done")
        
        else:
            print(form.errors)

    context = {
        "form": form,
    }

    return render(request, "myapp/username_change.html", context)

@login_required
def username_change_done(request):
    return render(request, "myapp/username_change_done.html")
    
class PasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("password_change_done")
    template_name ="myapp/password_change.html"

class PasswordChangeDone(PasswordChangeDoneView):
    template_name = "myapp/password_change_done.html"
