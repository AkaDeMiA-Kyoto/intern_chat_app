from django.shortcuts import redirect, render
from .models import CustomUser,Chat
from .forms import SignUpForm,LoginForm,message,MyPasswordChangeForm
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import LoginView,PasswordChangeView,PasswordChangeDoneView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


def index(request):
    return render(request, "myapp/index.html")

def setting(request):
    return render(request, "myapp/setting.html")

def form_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()

            return render(request,'myapp/index.html')
    else:
        form = SignUpForm()
    return render(request, 'myapp/signup.html', {'form': form})

def model_signup(request):
    if request.method == 'POST':
        form = CustomUser(request.POST,request.FILES)
        form.save()
        return render(request,'myapp/index.html')
        
    else:
        form = CustomUser()
    return render(request, 'myapp/signup.html', {'form': form})

class Loginview1(LoginView):
    authentication_form = LoginForm
    template_name = "myapp/login.html"
    
@login_required
def friends_view(request):
    user_now = request.user
    messages = Chat.objects.filter(Q(sender = user_now) | Q(receiver = user_now))

    if Chat.objects.filter(Q(sender = user_now) | Q(receiver = user_now)).exists():
        others_data = CustomUser.objects.exclude(id=user_now.id).order_by('-date_joined')
        latest_message_order_by_others_data = []
        has_messages = []
        not_has_messages = []
        for user in others_data:
            if messages.filter(Q(sender = user) | Q(receiver = user)).exists():
                has_messages.append(user)
                messages_of_user = messages.filter(Q(sender = user) | Q(receiver = user)).order_by('-time').first()
                latest_message_order_by_others_data.append(messages_of_user)
            else:
                not_has_messages.append(user)

        users_ordered = []
        for i in has_messages:
            users_ordered.append(i)
        for i in not_has_messages:
            users_ordered.append(i)
            latest_message_order_by_others_data.append(i)
        ziplist = zip(users_ordered,latest_message_order_by_others_data)
        content = {
            'zip':ziplist,
        }
        return render(request,'myapp/friends.html',content)

    else:
        others_data = CustomUser.objects.exclude(id=user_now.id).exclude(username='').exclude(username=None).order_by('-date_joined')
        content = {
            'users':others_data
        }

        return render(request,'myapp/friends.html',content)

@login_required
def talk_room_view(request,user_id):
    user_now = request.user
    friend = CustomUser.objects.exclude(id=user_now.id).order_by('date_joined').get(id=user_id)
    messages = Chat.objects.filter(Q(sender = user_now,receiver = friend) | Q(sender = friend,receiver = user_now)).order_by('time')
    if request.method == 'POST':
        form = message(request.POST)
        if form.is_valid():
            Chat.objects.create(
                sender = user_now,
                receiver = friend,
                content = form.cleaned_data['content'],
            )
        form = message()    
        content = {
            'form':form,
            'messages':messages,
            'talk_to':friend,
            'id':user_id,
        }
        return render(request,'myapp/talk_room.html',content)
    else:
        form = message()
        content = {
            'form':form,
            'messages':messages,
            'talk_to':friend,
            'id':user_id,
        }
    return render(request, 'myapp/talk_room.html', content)

class Change_username(UpdateView,LoginRequiredMixin):
    model = CustomUser
    fields = ('username',)
    template_name = 'myapp/change_username.html'
    success_url = reverse_lazy('myapp:friends')

class Change_email(UpdateView,LoginRequiredMixin):
    model = CustomUser
    fields = ('email',)
    template_name = 'myapp/change_email.html'
    success_url = reverse_lazy('myapp:friends')

class Change_icon(UpdateView,LoginRequiredMixin):
    model = CustomUser
    fields = ('img',)
    template_name = 'myapp/change_icon.html'
    success_url = reverse_lazy('myapp:friends')


class PasswordChange(PasswordChangeView,LoginRequiredMixin):
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('myapp:changedone')
    template_name = 'myapp/change_password.html'

class PasswordChangeDone(PasswordChangeDoneView,LoginRequiredMixin):
    template_name = 'myapp/change_done.html'




    



