from django.shortcuts import redirect, render, get_object_or_404
from .forms import SignUpForm, LoginForm, ChatForm, UsernameChangeForm, EmailChangeForm, IconChangeForm
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from .models import CustomUser, Message
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import UpdateView
from django.urls import reverse, reverse_lazy

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('myapp:index')
    else:
        form = SignUpForm()
    return render(request, 'myapp/signup.html', {'form':form})

class LoginView(LoginView):
    template_name = 'myapp/login.html'
    authentication_form = LoginForm

class LogoutView(LogoutView):
    template_name = 'myapp/logout.html'

@login_required
def friends(request):
    user = request.user
    friends = CustomUser.objects.all()
    friends_data = []
    for friend in friends:
        latest_message = Message.objects.filter(
            (Q(sender=user) & Q(receiver=friend)) |
            (Q(sender=friend) & Q(receiver=user))
        ).order_by('-time').first()
        friends_data.append({
            'friend':friend,
            'latest_message':latest_message
            })
    return render(request, "myapp/friends.html", {'user':user,'friends_data': friends_data})

def talk_room(request, pk):
    user = request.user
    friend = get_object_or_404(CustomUser, pk=pk)
    talk_log = Message.objects.filter(
        (Q(sender=user) & Q(receiver=friend)) |
        (Q(sender=friend) & Q(receiver=user))
    ).order_by('time')

    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = user
            message.receiver = friend
            message.save()
            return redirect("myapp:talk_room", pk=pk)
    else:
        form = ChatForm()

    return render(request, "myapp/talk_room.html", {
        'user':user, 
        'friend':friend, 
        'talk_log':talk_log,
        'form':form
    })

def setting(request, pk):
    return render(request, "myapp/setting.html")

class UsernameUpdateView(UpdateView):
    model = CustomUser
    form_class = UsernameChangeForm
    template_name = "myapp/setting_change.html"
        
    def get_success_url(self):
        return reverse('myapp:setting_success', kwargs={'pk': self.object.pk})

class EmailUpdateView(UpdateView):
    model = CustomUser
    form_class = EmailChangeForm
    template_name = "myapp/setting_change.html"
    
    def get_success_url(self):
        return reverse('myapp:setting_success', kwargs={'pk': self.object.pk})

class IconUpdateView(UpdateView):
    model = CustomUser
    form_class = IconChangeForm
    template_name = "myapp/setting_change.html"
    
    def get_success_url(self):
        return reverse('myapp:setting_success', kwargs={'pk': self.object.pk})
    
class MyPasswordChangeView(PasswordChangeView):
    template_name = "myapp/setting_change.html"
    
    def get_success_url(self):
        return reverse('myapp:password_success')
    
def password_success(request):
    return render(request, "myapp/password_success.html")

def setting_success(request, pk):
    return render(request, "myapp/setting_success.html", {'pk':pk})
