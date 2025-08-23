from django.shortcuts import redirect, render, get_object_or_404
from .forms import CustomUserCreationForm, SendMessageForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from .models import Message, CustomUser
from django.db.models import Q



def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.POST:
        form = CustomUserCreationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form' : form
    }
    return render(request, "myapp/signup.html", context)

class login_view(LoginView):
    template_name = 'myapp/login.html'

def friends(request):
    friends_list = CustomUser.objects.exclude(id = request.user.id).all()
    text_list = []
    for i in friends_list:
        if not Message:
            text_list.append(" ")
        else:    
            sentence = Message.objects.filter((Q(sender = i, receiver = request.user) | Q(receiver = i, sender = request.user))).order_by('-send_time').first()
            if sentence == None:
                text_list.append(" ")
            else:
                text_list.append(sentence)
    friend_text = zip(friends_list, text_list)
    context = {
        'text_list' : text_list,
        'friend_text' : friend_text
    }
    return render(request, "myapp/friends.html", context)

def talk_room(request, pk):
    the_other_user = get_object_or_404(CustomUser, pk = pk)
    messages = Message.objects.filter((Q(sender = request.user, receiver = the_other_user) | Q(sender = the_other_user, receiver = request.user))).order_by('send_time')
    if request.method == 'POST':
        form = SendMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit = False)
            message.receiver = the_other_user
            message.sender = request.user
            message.save()
            return redirect('talk_room', pk = pk)
    else:
        form = SendMessageForm()
    context = {
        'messages' : messages,
        'the_other_user' : the_other_user,
        'form' : form
    }
    return render(request, "myapp/talk_room.html", context)

def setting(request):
    return render(request, "myapp/setting.html")

