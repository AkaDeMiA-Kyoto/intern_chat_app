from django.shortcuts import redirect, render, get_object_or_404
from .forms import SignUpForm, LoginForm, ChatMessageForm
from django.contrib.auth.views import LoginView
from django.views import View
from .models import CustomUser, TalkLog
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q



def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("myapp:index")
        return render(request, "myapp/signup.html", {"form": form})
    elif request.method == 'GET':
        form = SignUpForm()
        return render(request, "myapp/signup.html", {"form": form})

class Login_View_Class(LoginView):
    template_name = 'myapp/login.html'
    form_class = LoginForm

login_view = Login_View_Class.as_view()

class FriendsView(LoginRequiredMixin, View):
    def get(self, request):
        friend_list = CustomUser.objects.all()
        latestlogs =[]
        talked_friend_list =[]
        for friend in friend_list:
            try:
                log = TalkLog.objects.filter(Q(touser = friend, fromuser = request.user) |  Q(touser = request.user, fromuser = friend)).order_by('-timestamp').first()
            except:
                print("トークログがありません。")
            else:
                if(log != None):
                    latestlogs.append(log)
                    talked_friend_list.append(friend)

        context={
            "friend_list":friend_list,
            "talked_friend_list":talked_friend_list, 
            "latestlogs":latestlogs,
        }

        return render(request, "myapp/friends.html", context)

friends_view = FriendsView.as_view()
# def friends(request):
#     friend_list = CustomUser.objects.all()
#     return render(request, "myapp/friends.html", {"friend_list":friend_list})

class TalkRoomView(LoginRequiredMixin, View):
    def get(self, request, id):
        touser = get_object_or_404(CustomUser, id=id)
        form = ChatMessageForm()
        talklog = TalkLog.objects.filter(Q(touser = touser, fromuser = request.user) |  Q(touser = request.user, fromuser = touser)).order_by('timestamp')
        return render(request, "myapp/talk_room.html", {"To_user": touser, "form": form, "talklog": talklog})
    
    def post(self, request, id):
        form = ChatMessageForm(request.POST)
        touser = get_object_or_404(CustomUser, id=id) 
        if form.is_valid():
            TalkLog.objects.create(
                message=form.cleaned_data['message'],
                touser=touser,
                fromuser=request.user
            )
            return redirect(request.path)
        else:
            return render(request, "myapp/talk_room.html", {"To_user": touser, "form": form})

talk_room = TalkRoomView.as_view()

# def talk_room(request, id):
#     user = get_object_or_404(CustomUser, id=id)
#     return render(request, "myapp/talk_room.html", {"user": user})

def setting(request):
    return render(request, "myapp/setting.html")


class SettingView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "myapp/setting.html")
