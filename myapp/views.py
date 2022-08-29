from importlib.resources import contents
from multiprocessing import context
from django.shortcuts import redirect, render
from .models import CustomUser
from .forms import SignUpForm,LoginForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    context = {
        'form' : SignUpForm(),
        'msg' : 'Good',
    }
    if request.method == 'POST':
        obj = CustomUser()
        form = SignUpForm(request.POST,request.FILES,instance = obj)
        if form.is_valid():
            form.save()
            context['form'] = SignUpForm(request.POST,request.FILES)
            return redirect(to='/')
        else:
            context['form'] = SignUpForm(request.POST,request.FILES)
            context["msg"] = 'bad'
    return render(request, "myapp/signup.html",context)

class login_view(LoginView):
    template_name = 'myapp/login.html'
    form_class = LoginForm

@login_required
def friends(request):
    context = {
        'user' : request.user
    }
    return render(request, "myapp/friends.html",context)

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
