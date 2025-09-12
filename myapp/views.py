from django.shortcuts import redirect, render
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = SignUpForm()

    return render(request, 'myapp/signup.html', {'form': form})

# def login_view(request):
#     return render(request, "myapp/login.html")

class login_view(LoginView):
    # ログイン画面のテンプレートを指定
    template_name = 'myapp/login.html'

    # ログイン成功後のリダイレクト先URL名を指定
    authentication_form = AuthenticationForm

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
