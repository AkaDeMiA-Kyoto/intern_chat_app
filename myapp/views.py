from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from .forms import SignupForm,CustomAuthenticationForm


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == "GET":
        form = SignupForm()
        return render(request, "myapp/signup.html", {"form": form}) #formを描画
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES) #POSTデータをformに保存
        if form.is_valid():
            form.save()
            return render(request, "myapp/index.html")
        else:
            form = SignupForm(request.POST, request.FILES)
            return render(request, "myapp/signup.html", {"form": form})


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm

def login_view(request):
    return CustomLoginView.as_view(template_name="myapp/login.html")(request)

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")


