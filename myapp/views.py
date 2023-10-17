import operator

from django.shortcuts import redirect, render, get_object_or_404

from django.contrib.auth.forms import UserCreationForm

from django.views.generic.edit import CreateView 

from .forms import (
    SignUpForm, 
    LoginForm, 
    TalkForm, 
    PasswordChangeForm,
    UsernameResetForm,
    MailResetForm,
    IconResetForm,
    FriendSearchForm,
)

from django.contrib.auth import get_user_model, login, logout

from .models import CustomUser, Talk

from django.db.models import Q

from django.contrib.auth.decorators import login_required

User = get_user_model()

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == "GET":
        form = SignUpForm()
        error_message = ''
    elif request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(to='index')

        else:
            print(form.errors)

    context = {
        "form": form,
    }
    return render(request, "myapp/signup.html",context)

def login_view(request):
    if request.method == "GET":
        form = LoginForm()
        error_message= ''
    elif request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
            return redirect(to='friends')

    else:
        form = LoginForm()

    context = {
        "form": form,
    }

    return render(request, "myapp/login.html",context)

@login_required
def friends(request):
    user = request.user
    friends = CustomUser.objects.exclude(id=user.id)
    searchForm = FriendSearchForm(request.GET)
    if request.method == "GET":
        if searchForm.is_valid():
            keyword = searchForm.cleaned_data['keyword']
            friends = friends.filter(username__contains=keyword)
        else:
            searchForm = FriendSearchForm()
            friends = friends.all()            

    info = []
    info_message = []
    info_no_message = []

    for friend in friends:
        new_message = Talk.objects.filter(
            Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend)
        ).order_by('time').last()

        if new_message:
            info_message.append([friend, new_message.talk, new_message.time])
        else:
            info_no_message.append([friend, None, None])
    
    info_message = sorted(info_message, key=operator.itemgetter(2),reverse=True)
  
    info.extend(info_message)
    info.extend(info_no_message)
  
    context={
        "info":info,
        'friends': friends,
        'searchForm': searchForm,
    }
    return render(request, "myapp/friends.html", context)


@login_required
def talk_room(request, user_id):
    user = request.user
    friend = get_object_or_404(CustomUser, id=user_id)
    talk = Talk.objects.filter(
        Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend)
    ).order_by("time")
    form = TalkForm()
    context = {
        "form": form,
        "talk": talk,
        "friend": friend,
    }

    if request.method == "POST":
        new_talk = Talk(talk_from=user, talk_to=friend)
        form = TalkForm(request.POST, instance=new_talk)

        if form.is_valid():
            form.save()
            return redirect("talk_room", user_id)
        else:
            print(form.errors)

    return render(request, "myapp/talk_room.html", context)

@login_required
def setting(request):
    return render(request, "myapp/setting.html")

@login_required
def username_change(request):
    user = request.user
    if request.method == "GET":
        form = UsernameResetForm(instance=user)
          
    elif request.method == "POST":
        form = UsernameResetForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(to="username_change_done")
            
        else:
            print(form.errors)

    context = {
        "form":form,
    }
    return render(request, "myapp/username_change.html", context)

@login_required
def username_change_done(request):
    return render(request, "myapp/username_change_done.html")

@login_required
def mail_change(request):
    user = request.user
    if request.method == "GET":
        form = MailResetForm(instance=user)

    elif request.method == "POST":
        form = MailResetForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("mail_change_done")
        
        else:
            print(form.errors)
    
    context = {
        "form":form
    }
    return render(request, "myapp/mail_change.html",context)

@login_required
def mail_change_done(request):
    return render(request, "myapp/mail_change_done.html")

@login_required
def icon_change(request):
    user = request.user
    if request.method == "GET":
        form = IconResetForm(instance=user)
    
    elif request.method == "POST":
        form = IconResetForm(request.POST, request.FILES,  instance=user)
        if form.is_valid():
            form.save()
            return redirect(to="icon_change_done")
        else:
            print(form.errors)
    
    context = {
        "form": form
    }
    return render(request, "myapp/icon_change.html", context)

@login_required
def icon_change_done(request):
    return render(request, "myapp/icon_change_done.html")

@login_required
def password_change(request):
    user = request.user
    if request.method == "GET":
        form = PasswordChangeForm(request.user)

    elif request.method == "POST":
        form = PasswordChangeForm(request.POST, request.user)
        if form.is_valid():
            form.save()
            return redirect(to='password_change_done')

        else:
            print(form.errors)

    context = {
        "form": form,
    }

    return render(request, "myapp/password_change.html", context)

@login_required
def password_change_done(request):
    return render(request, "myapp/password_change_done.html")

@login_required
def logout_view(request):
    logout(request)
    redirect(to='index')
    return render(request, "myapp/index.html")