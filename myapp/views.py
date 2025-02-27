from django.shortcuts import redirect, render
from .forms import SignUpForm, LoginForm
from django.contrib.auth.views import LoginView
from .models import CustomUser


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

def friends(request):
    friend_list = CustomUser.objects.all()
    return render(request, "myapp/friends.html", {"friend_list":friend_list})

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
