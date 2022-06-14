import operator

from django.shortcuts import redirect, render, get_object_or_404
from .forms import LoginForm, SignUpForm
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.db.models import Q


from .models import Talk

User = get_user_model()

def index(request):
    return render(request, "myapp/index.html")

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.FILES)
            form.save()
            return redirect("index")
    else:
        form = SignUpForm()
    params = {
        'form': form,
    }
    return render(request, "myapp/signup.html", params)

class Login(LoginView):
    authentication_form = LoginForm
    template_name = "myapp/login.html"

class Logout(LogoutView):
    template_name = "myapp/index.html"

@login_required
def friends(request):
    user = request.user
    # requestの中にuserのattributeが存在し、ログインしている使用者を特定するインスタンスが存在
    friends = User.objects.exclude(id=user.id)

    info = []
    info_have_message = []
    info_have_no_message = []

    for friend in friends:
        latest_message = Talk.objects.filter(
            Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend)
        ).order_by('time').last()

        if latest_message:
            info_have_message.append([friend, latest_message.talk, latest_message.time])
        else:
            info_have_no_message.append([friend, None, None])


    info_have_message = sorted(info_have_message, key=operator.itemgetter(2), reverse=True)
    # info_have_messageの三番目の要素を基準にして、info_have_messageを降順に並べ替える

    info.extend(info_have_message)
    info.extend(info_have_no_message)
    # infoリストにinfo_have_messageリストを追加
    # infoリストにinfo_have_no_messageリストを追加

    content = {
        "info": info,
    }
    return render(request, "myapp/friends.html", content)


def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
