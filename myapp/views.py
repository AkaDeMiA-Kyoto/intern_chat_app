from django.shortcuts import redirect, render, get_object_or_404
from .models import CustomUser, Friend
from .forms import SignupForm, MessageForm, UsernameChangeForm, EmailChangeForm, IconChangeForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Q, Subquery, Max


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = SignupForm()
    param = {'form' : form}
    return render(request, 'myapp/signup.html', param)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user) 
                return redirect('friends')
    else:
        form = AuthenticationForm()
    param = {'form' : form}
    return render(request, "myapp/login.html",param)

@login_required
def friends(request):
    User = get_user_model()
    current_user = request.user
    latest_messages = Friend.objects.filter(
        Q(sender = current_user, recipient = OuterRef('pk')) | Q(sender = OuterRef('pk'), recipient = current_user)
    ).order_by('-created_at')
    other_users = User.objects.exclude(pk = current_user.pk).annotate(
        last_message_content=Subquery(latest_messages.values('content')[:1])
    ).order_by('pk')
    context = {
        'other_users': other_users
    }
    return render(request, "myapp/friends.html", context)

@login_required
def talk_room(request, recipient_pk):
    User = get_user_model()
    sender = request.user
    recipient = get_object_or_404(User, pk = recipient_pk)
    messages = Friend.objects.filter(
        Q(sender = sender, recipient = recipient) | Q(sender = recipient, recipient = sender)
    ).order_by('created_at')
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit = False)
            message.sender = request.user
            message.recipient = recipient
            message.save()
            return redirect('talk_room', recipient_pk = recipient.pk)
    else:
        form = MessageForm()
    context = {
        'messages' : messages,
        'recipient' : recipient,
        'form' : form
    }
    return render(request, "myapp/talk_room.html", context)

def setting(request):
    return render(request, "myapp/setting.html")

@login_required
def username_change_view(request):
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('changed')
    else:
        form = UsernameChangeForm(instance = request.user)
    
    return render(request, 'myapp/username_change.html', {'form': form})

@login_required
def email_change_view(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('changed')
    else:
        form = EmailChangeForm(instance = request.user)
    
    return render(request, 'myapp/email_change.html', {'form': form})

@login_required
def icon_change_view(request):
    if request.method == 'POST':
        form = IconChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('changed')
    else:
        form = IconChangeForm(instance=request.user)
    
    return render(request, 'myapp/icon_change.html', {'form': form})

@login_required
def changed(request):
    return render(request, 'myapp/changed.html')