from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from .forms import LoginForm
from django.views.generic import TemplateView
from django.contrib.auth.hashers import make_password


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    return render(request, "myapp/signup.html")

def login_view(request):
    return render(request, "myapp/login.html")

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
from django.shortcuts import redirect, render
from .models import CustomUser
from . import forms
from .forms import SingupForm


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    form = forms.SingupForm()
    return render(request, "myapp/signup.html", {'form': form})

def login_view(request):
    return render(request, "myapp/login.html")

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")

def register(request):
    if request.method == 'POST':
        form = SingupForm(request.POST,request.FILES)
        if form.is_valid():
            print('ok')
            # ユーザー登録
            CustomUser.objects.create(
                username=request.POST['username'], 
                email=request.POST['email'], 
                password=make_password(request.POST['password']), 
                icon_image=request.FILES['image']
                )
            return redirect('index')
        else:
            print('is not ok')
            answer = form
            form = SingupForm()
            context = {
                'form' : form,
                'answer' : answer
            }
            return render(request, "myapp/signup.html", context)

# 参考
# https://kamatimaru.hatenablog.com/entry/2020/05/12/060236

# https://marsquai.com/745ca65e-e38b-4a8e-8d59-55421be50f7e/05f253f8-c11b-4c91-8091-989eb2600a7b/de4d464b-1e55-47f4-b993-85dad837dcab/

class Login(LoginView):
    form_class = LoginForm
    template_name = 'myapp/login.html'

class Friends(LoginRequiredMixin, TemplateView):
    template_name = 'myapp/friends.html'
