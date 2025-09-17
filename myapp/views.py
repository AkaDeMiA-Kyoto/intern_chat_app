from django.shortcuts import redirect, render
from .forms import SignupForm, LoginForm, TalkModelForm, UsernameChangeForm, EmailChangeForm, IconChangeForm
from django.contrib.auth import login
from .models import CustomUser, Talk
from django.db.models import Q
from datetime import datetime,timezone



def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, 'myapp/index.html')


    else:
        form = SignupForm()
    
    param = {
        'form': form
    }

    return render(request, 'myapp/signup.html', param)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            if user:
                login(request, user)
                return redirect('/friends')

    else:
        form = LoginForm()

    param = {
        'form': form,
    }

    return render(request, "myapp/login.html", param)

def friends(request):
    friends_list = CustomUser.objects.exclude(id=request.user.id)
    user = request.user
    latest_messages=[]
    for friend in friends_list:
        latest_message = Talk.objects.filter(Q(talk_from=user, talk_to=friend) | Q(talk_from=friend, talk_to=user)).order_by('-pub_date').first()
        latest_messages.append([friend,latest_message])
    aware_min_utc = datetime.min.replace(tzinfo=timezone.utc)
    talk_rooms = sorted(latest_messages, key=lambda x: (x[1].pub_date if x[1] is not None else aware_min_utc, x[0].id) , reverse=True)
    context = {
        'friends_list': friends_list,
        'latest_message': latest_message,
        "latest_messages":latest_messages,
        "talk_rooms":talk_rooms
    }
    return render(request, "myapp/friends.html", context)

def talk_room(request, friend_id):
    user = request.user
    
    friend = CustomUser.objects.get(id=friend_id)
    talk_list = Talk.objects.filter(Q(talk_from=user, talk_to=friend) | Q(talk_from=friend, talk_to=user)).order_by("pub_date")
    form = TalkModelForm()

    if request.method == 'POST':
        form = TalkModelForm(request.POST)
        if form.is_valid():
            talk = form.save(commit=False)
            talk.talk_from = user
            talk.talk_to = friend
            talk.save()
            return redirect('talk_room', friend_id)
            

    context = {
        'user': user,
        'friend': friend,
        'form': form,
        'talk_list': talk_list,
    }

    return render(request, "myapp/talk_room.html", context)

def setting(request):


    return render(request, "myapp/setting.html")

def username_change(request):
    user = request.user
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST)
        if form.is_valid():
            new_username = form.cleaned_data['username']
            user.username = new_username
            user.save()
            return redirect('username_change_done')
    else:
        form = UsernameChangeForm()
    return render(request, "myapp/username_change.html", {'form': form})

def username_change_done(request):
    return render(request, "myapp/username_change_done.html")

def email_change(request):
    user = request.user
    if request.method == 'POST':
        form = EmailChangeForm(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data['email']
            user.email = new_email
            user.save()
            return redirect('email_change_done')
    else:
        form = EmailChangeForm()
    return render(request, "myapp/email_change.html", {'form': form})

def email_change_done(request):
    return render(request, "myapp/email_change_done.html")

def icon_change(request):
    user = request.user
    if request.method == 'POST':
        form = IconChangeForm(request.POST, request.FILES)
        if form.is_valid():
            new_icon = form.cleaned_data['icon']
            user.icon = new_icon
            user.save()
            return redirect('icon_change_done')
    else:
        form = IconChangeForm(initial={'icon': user.icon})
    return render(request, "myapp/icon_change.html", {'form': form})

def icon_change_done(request):
    return render(request, "myapp/icon_change_done.html")

def password_change(request):
    return render(request, "myapp/password_change.html")

def password_change_done(request):
    return render(request, "myapp/password_change_done.html")

def logout(request):
    return render(request, "myapp/index.html")



