from django.shortcuts import redirect, render
from .forms import SignUpForm
from django.views.generic.edit import CreateView
from .models import CustomUser
from django.urls import reverse_lazy
from .forms import LoginForm
from django.contrib.auth.views import LoginView
#from .models import Talk

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    return render(request, "myapp/signup.html")

def login_view(request):
    return render(request, "myapp/login.html")

def friends(request):
    users = CustomUser.objects.all()
    sorted_users = users.order_by('-date_joined')
    #for user in users:
    #    latest_talk = user.talks.order_by('-timestamp').first()  # 最新のトークを取得
    #    user.latest_talk = latest_talk
    return render(request, "myapp/friends.html", {'users': users})

def talk_room(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, "myapp/talk_room.html", {'user': user})

def setting(request):
    return render(request, "myapp/setting.html")

class SignUpView(CreateView):
    template_name="myapp/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy('index')

class loginview(LoginView):
    template_name="myapp/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('friends')

