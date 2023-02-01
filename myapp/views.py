from django.shortcuts import redirect, render


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
                password=request.POST['password'], 
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
