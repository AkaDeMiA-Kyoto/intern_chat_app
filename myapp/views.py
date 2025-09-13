from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views import View

from .forms import SignUpForm
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from  .forms import LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import talk,CustomUser
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import UserIconForm,UserNameForm,UserMailForm
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    return render(request, "myapp/signup.html")

def login_view(request):
    return render(request, "myapp/login.html")


def setting(request):
    return render(request, "myapp/setting.html")

@login_required
def profile(request):
    return render(request, template_name="accounts/profile.html")


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("index")
    template_name = "myapp/signup.html"

    # def form_valid(self, form):
    #     user = form.save()
    #     login(self.request, user)
    #     self.object = user
    #     return redirect(self.get_success_url())class HomeView(LoginRequiredMixin, TemplateView):#「LoginRequiredMixin → TemplateView」この順番で記述しないとログイン必須機能が表れないので注意！！
class Login(LoginView):
    template_name = 'myapp/login.html'
    form_class = LoginForm
    login_url = '/login/'
def friends(request):
    my_user = request.user
    all_talks = talk.objects.filter(
        Q(sender=my_user) | Q(recipient=my_user)
    ).order_by('-created_at')
    talks_by_partner = {}
    for t in all_talks:
        partner = t.sender if t.sender != my_user else t.recipient
        if partner.id not in talks_by_partner:
            talks_by_partner[partner.id] = {
                'partner': partner,
                'last_talk': t,
            }

    context = {
        'friends': talks_by_partner.values()
    }
    return render(request, 'myapp/friends.html', context)

def talk_room(request, friend_id):
    my_user=request.user
    talk_partner = get_object_or_404(CustomUser, id=friend_id)
    talks=talk.objects.filter((
        Q(sender=my_user, recipient=talk_partner) | Q(sender=talk_partner, recipient=my_user)
    )).order_by('created_at')
    context={
        'my_user':my_user,
        'talk_partner':talk_partner,
        'talks':talks,
    }
    return render(request, 'myapp/talk_room.html', context)
def send_talk(request, friend_id):
    if request.method == 'POST':
        sender = request.user
        recipient = get_object_or_404(CustomUser, id=friend_id)
        content = request.POST.get('content')
        
        if content:
            talk.objects.create(
                sender=sender,
                recipient=recipient,
                content=content
            )
    return redirect('talk_room', friend_id=friend_id)
class ChangeIconView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserIconForm(instance=request.user)
        return render(request, 'myapp/icon_change.html', {'form': form})

    def post(self, request):
        form = UserIconForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('icon_change_done')
        return render(request, 'myapp/icon_change.html', {'form': form})
def icon_change_done(request):
    return render(request, 'myapp/icon_change_done.html')

class ChangeNameView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserNameForm(instance=request.user)
        return render(request, 'myapp/username_change.html', {'form': form})

    def post(self, request):
        form = UserNameForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('username_change_done')
        return render(request, 'myapp/username_change.html', {'form': form})
def username_change_done(request):
    return render(request, 'myapp/username_change_done.html')

class ChangeMailView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserMailForm(instance=request.user)
        return render(request, 'myapp/mail_change.html', {'form': form})

    def post(self, request):
        form = UserMailForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('mail_change_done')
        return render(request, 'myapp/mail_change.html', {'form': form})
def mail_change_done(request):
    return render(request, 'myapp/mail_change_done.html')