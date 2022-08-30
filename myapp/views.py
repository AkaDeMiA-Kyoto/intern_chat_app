from multiprocessing import context
from django.shortcuts import redirect, render
from .models import CustomUser,Chat
from .forms import FriendSearchForm, SignUpForm,LoginForm,ChatSendForm,UpDateForm
from django.contrib.auth.views import LoginView,LogoutView
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

class login_view(LoginView,LoginRequiredMixin):
    template_name = 'myapp/login.html'
    form_class = LoginForm

class logout_view(LogoutView):
    template_name = 'myapp/index.html'

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
        context['data'] = CustomUser.objects.filter(username__icontains=request.POST['find']).exclude(
            Q(id = user.id) | Q(id = 1)
        )
        context['form'] = FriendSearchForm(request.POST)
    return render(request, "myapp/friends.html",context)

def talk_room(request,id):
    user = request.user
    context = {
        'data' : Chat.objects.filter(
            Q(chat_to = user, chat_from = CustomUser.objects.get(id=id)) | Q(chat_to = CustomUser.objects.get(id=id).id, chat_from = user)
        ).order_by('pub_date'),
        'form' : ChatSendForm(),
        'id' : id,
        'friend_name' : CustomUser.objects.get(id=id).username,
    }
    if request.method == 'POST':
        obj = Chat(chat_to = CustomUser.objects.get(id = id),chat_from = user)
        form = ChatSendForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            context['form'] = ChatSendForm()
        else:
            context['msg'] = 'Bad'
    return render(request, "myapp/talk_room.html",context)

def setting(request):
    return render(request, "myapp/setting.html")

def update(request):
    user = request.user
    context = {
        'form' : UpDateForm(instance=user),
        'msg' : 'Good',
    }
    if request.method == 'POST':
        obj = user
        form = UpDateForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            context['form'] = UpDateForm(request.POST)
        else:
            context['msg'] = 'Bad'
    return render(request, 'myapp/update.html',context)
