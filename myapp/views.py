from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import redirect, render
from .forms import EmailChangeForm, ImageChangeForm, MessageForm, SignupForm, LoginForm, PasswordChangeForm, UsernameChangeForm
from .models import Message, User
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

def index(request):
    return render(request, "myapp/index.html")

def signup(request):
    parameters = {}

    if request.method == 'GET':
        parameters['form'] = SignupForm()
    elif request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(to="/")
        parameters['form'] = form
        
    return render(request, "myapp/signup.html", parameters)


class login(LoginView):   
    form_class = LoginForm
    template_name = "myapp/login.html"

class logout(LogoutView, LoginRequiredMixin):
    pass

@login_required
def friends(request):
    parameters = {}
    parameters['friends'] = User.objects.filter(~Q(username=request.user.username))
    return render(request, "myapp/friends.html", parameters)

@login_required
def talk_room(request, partner):
    parameters = {}
    user_id = request.user.unique_id
    try:
        partner_id = User.objects.get(username=partner).unique_id
    except ObjectDoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = Message(
                sender=user_id, \
                receiver=partner_id, \
                contents=form.cleaned_data['contents']
            )
            message.save()

    parameters['messages'] = Message.objects.filter(Q(sender=partner_id, receiver=user_id) | Q(sender=user_id, receiver=partner_id)) 
    parameters['form'] = MessageForm() # 文字さえ入力していれば基本validateは通る気がするのでrequest.POSTは入れない
    parameters['partner'] = partner
    parameters['partner_id'] = partner_id
    return render(request, "myapp/talk_room.html", parameters)

@login_required
def setting(request):
    return render(request, "myapp/setting.html")

def PostForm(item, request):
    user = request.user
    if item == 'username':
        return UsernameChangeForm(request.POST, instance=user)
    elif item == 'email':
        return EmailChangeForm(request.POST, instance=user)
    else:
        return ImageChangeForm(request.POST, request.FILE, instance=user)

def GetForm(item, request):
    user = request.user
    if item == 'username':
        return UsernameChangeForm(instance=user)
    elif item == 'email':
        return EmailChangeForm(instance=user)
    else:
        return ImageChangeForm(instance=user)

@login_required
def change(request, item):
    parameters = {}

    if item not in { 'username', 'email', 'image' }:
        raise Http404

    if request.method == 'POST':
        form = PostForm(item, request)
        if form.is_valid():
            form.save()
            return redirect(to=item+"/done")

    parameters['item'] = item
    parameters['form'] = GetForm(item, request)
    return render(request, "myapp/change.html", parameters)

class password_change(PasswordChangeView, LoginRequiredMixin):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("myapp:change_done", kwargs={'item':'password'})
    template_name = "myapp/change.html"

@login_required
def change_done(request, item):
    return render(request, "myapp/change_done.html")
