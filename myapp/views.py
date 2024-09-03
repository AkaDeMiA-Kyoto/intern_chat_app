from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from .forms import SignupForm, LoginForm

from .models import CustomUser, Message


# def index(request):
#     return render(request, "myapp/index.html")

class IndexView(TemplateView):
    """ ホームビュー """
    template_name = "myapp/index.html"


def signup(request):
    if request.POST:
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('myapp:login')
    else:
        form = SignupForm()
    return render(request, "myapp/signup.html", {'form': form})


class UserSignupView(CreateView):
    """ ユーザー登録用ビュー """
    form_class = SignupForm
    template_name = "myapp/signup.html"
    success_url = reverse_lazy("myapp:signup")


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'myapp/login.html'
    redirect_field_name = REDIRECT_FIELD_NAME

    # def form_valid(self, form):
    #     form.instance.customuser_id = self.kwargs['customuser_pk']
    #     customuser = get_object_or_404(CustomUser, pk=)
    #     return redirect('myapp/friends', {'customuser': customuser})


@login_required
def friends(request):
    user = request.user
    talk_info = []
    friends = CustomUser.objects.exclude(username=request.user.username)
    for friend in friends:
        latest_message = Message.objects.filter(
            Q(message_from=user, message_to=friend) |
            Q(message_from=friend, message_to=user)
        ).order_by("-sent_at").first()
        icon = friend.image
        if latest_message:
            talk_info.append(
                [
                    icon,
                    friend,
                    latest_message.message,
                    latest_message.sent_at
                ]
            )
        else:
            talk_info.append(
                [
                    icon,
                    friend,
                    None,
                    None
                ]
            )
            # msg_dict = {}
            # customuser = CustomUser.objects.all().order_by('date_joined')
            # print(customuser)
            # for user in customuser:
            #     latest_message = Message.objects.filter(user=user).order_by("-sent_at").first()
            #     msg_dict[user] = latest_message
            #     latest_messages.append(latest_message)
            # print(latest_message)
            # print(latest_messages)
            # message = customuser.message_set.all()
            context = {
                'talk_info': talk_info
            }
    return render(request, "myapp/friends.html", context)

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
