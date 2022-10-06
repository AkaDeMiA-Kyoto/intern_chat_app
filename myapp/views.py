from audioop import reverse
from importlib.resources import contents
from django.shortcuts import redirect, render, get_object_or_404

from myapp.models import CustomUser, Talk
from myapp.utils import create_latest_talk
from .forms import NameChangeForm, SignUpForm, LoginForm, TalkForm, PasswordChangingForm, NameChangeForm, MailChangeForm, IconChangeForm
#from django.views.generic.edit import CreateView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, LogoutView #LoginView,  
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import Q
from .utils import create_latest_talk

from allauth.account.views import ConfirmEmailView

def index(request):
    return render(request, "myapp/index.html")

#@login_required
#def friends(request):

    if request.method == 'POST':
        form = FindForm(request.POST)
        find = request.POST['find']
        data = CustomUser.objects.filter(username__contains=find)

    else:
        data = CustomUser.objects.all()
    #.values('img', 'username')
        params = {
            'data' : data
        }
        
    return render(request, "myapp/friends.html", params)
    
@login_required
def friends(request):

    user = request.user

    talk = create_latest_talk(user)

    find = request.GET.get("query")

    if find:
        friend = friend.filter(username__contains=find)
        talk = create_latest_talk(user)

    params = {
        'talk' : talk,
    }
    return render(request, "myapp/friends.html", params)



@login_required
def talk_room(request, pk):
    user = request.user
    friend = get_object_or_404(CustomUser, id=pk)
    data = Talk.objects.filter( Q(talk_from=user, talk_to=friend) | Q(talk_from=friend, talk_to=user) ).order_by('talk_at')
    form = TalkForm()
    params = {
        'data' : data,
        'friend' : friend,
        'form' : form,
    }

    if request.method == 'POST':
        new_talk = Talk(talk_to=friend, talk_from=user)
        form = TalkForm(request.POST, instance=new_talk)

        if form.is_valid():
            form.save()
            return redirect("talk_room", pk)

        else:
            print(TalkForm.errors)

    return render(request, "myapp/talk_room.html", params)

def setting(request):
    return render(request, "myapp/setting.html")


#class Signup(CreateView):
    form_class = SignUpForm
    template_name = "myapp/signup.html" 
    success_url = reverse_lazy('index')


#class Login(LoginView):
    form_class = LoginForm
    template_name = 'myapp/login.html'


class PasswordChange(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('pass_change_done')
    template_name = 'myapp/pass_change.html'


def pass_change_done(request):
    return render(request, 'myapp/pass_change_done.html')


@login_required
def name_change(request):
    user = request.user
    if request.method == "GET":
        form = NameChangeForm(instance=user)

    elif request.method == 'POST':
        form = NameChangeForm(request.POST, instance=user)
        if form.is_valid:
            form.save()
            return redirect("name_change_done")
        else:
            print(form.errors)

    params = {
        "form": form,
    } 
        
    return render(request, 'myapp/name_change.html', params)

@login_required
def name_change_done(request):
    return render(request, 'myapp/name_change_done.html')



@login_required
def mail_change(request):
    user = request.user
    if request.method == "GET":
        form = MailChangeForm(instance=user)

    elif request.method == 'POST':
        form = MailChangeForm(request.POST, instance=user)
        if form.is_valid:
            form.save()
            return redirect("mail_change_done")
        else:
            print(form.errors)

    params = {
        "form": form,
    } 
        
    return render(request, 'myapp/mail_change.html', params)

@login_required
def mail_change_done(request):
    return render(request, 'myapp/mail_change_done.html')


@login_required
def icon_change(request):
    user = request.user
    if request.method == "GET":
        form = IconChangeForm(instance=user)

    elif request.method == 'POST':
        form = IconChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid:
            form.save()
            return redirect("icon_change_done")
        else:
            print(form.errors)

    params = {
        "form": form,
    } 
        
    return render(request, 'myapp/icon_change.html', params)

@login_required
def icon_change_done(request):
    return render(request, 'myapp/icon_change_done.html')


class Logout(LogoutView):
    template_name = 'myapp/logout.html'
