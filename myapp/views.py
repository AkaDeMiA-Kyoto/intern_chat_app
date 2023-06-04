from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from .forms import SignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser, Message
import pytz
from .functions import get_view_date
from django.db.models import Q

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("index")
    else:
        form = SignUpForm()
    return render(request, "myapp/signup.html", {"form": form})

class Login(LoginView):
    template_name = "myapp/login.html"

class Friends(LoginRequiredMixin, TemplateView):
    template_name = "myapp/friends.html"

    def get_context_data(self, **kwargs): # ?理解
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        otherusers = CustomUser.objects.exclude(username=self.request.user.username)
        for otheruser in otherusers:
            if Message.objects.filter(user_from=otheruser.id) or Message.objects.filter(user_to=otheruser.id):
                recent_talk = (Message.objects.filter(user_from=otheruser.id) | Message.objects.filter(user_to=otheruser.id)).latest("date")
                otheruser.date = recent_talk.date.astimezone(pytz.timezone('Asia/Tokyo'))
                otheruser.message = recent_talk.message
            else:
                otheruser.date = otheruser.date_joined.astimezone(pytz.timezone('Asia/Tokyo'))
                otheruser.message = "You have not talked yet."
            otheruser.view_date = get_view_date(otheruser.date)
            otheruser.save()
        context['users'] = otherusers.all().order_by("-date")
        return context

class TalkRoom(LoginRequiredMixin, TemplateView):
    template_name = "myapp/talk_room.html"

class Setting(LoginRequiredMixin, TemplateView):
    template_name = "myapp/setting.html"