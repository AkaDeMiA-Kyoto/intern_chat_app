from importlib.resources import contents
from multiprocessing import context
from django.shortcuts import redirect, render
from .models import CustomUser
from .forms import FriendSearchForm, SignUpForm,LoginForm
from django.contrib.auth.views import LoginView
from django.db.models import Q
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
    user = request.user
    context = {
        'user' : request.user,
        'data' : CustomUser.objects.exclude(
            Q(id = user.id) | Q(id = 1)
        ),
        'form' : FriendSearchForm()
    }
    if request.method == 'POST':
        context['data'] = CustomUser.objects.filter(username__iconstrains=request.POST['find']).exclude(
            Q(id = user.id) | Q(id = 1)
        )
        context['form'] = FriendSearchForm(request.POST)
    return render(request, "myapp/friends.html",context)

def talk_room(request,id):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
