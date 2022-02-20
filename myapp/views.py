from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignUpForm,TalkForm,UsernameForm,MailForm,PasswordForm,UpdateForm
from django.contrib.auth.views import LoginView,PasswordChangeView,LogoutView
from .models import TalkModel,User
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView,UpdateView,DeleteView
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib import messages



@login_required
def home(request):
    return render(request, 'myapp/home.html')

class SignupView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = "myapp/signup.html"
    success_url = reverse_lazy('friends')

    def form_valid(self,form):
        user = form.save()
        login(self.request, user,backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self,form):
        messages.error(self.request,"失敗")
        return super().form_invalid(form)


def index(request):

    return render(request, "myapp/index.html")


class login_view(LoginView):
    authentication_form = LoginForm
    template_name = "myapp/login.html"
    success_url = reverse_lazy('friends')


@login_required
def friends(request):
    login_user = request.user
    data = User.objects.exclude(id = login_user.id)
    params = {'data':data,'login_user':login_user}
    return render(request, 'myapp/friends.html', params)

@login_required
def talk_room(request,user_id,friend_id):
    user = User.objects.get(id = user_id)
    friend = User.objects.get(id = friend_id)
    talk = TalkModel.objects.filter(Q(sender = user,talkname = friend)|Q(sender = friend,talkname = user))
    talkform = TalkForm()
    params = {'friend':friend,'talk':talk,'form':talkform}
    
    if request.method == 'POST':
        talkform = TalkForm(request.POST)
        if talkform.is_valid:
            talkform.instance.sender = user
            talkform.instance.talkname = friend
            talkform.save()
        return redirect('talk_room',user_id,friend_id)

    return render(request,'myapp/talk_room.html',params)

@login_required
def setting(request):
    return render(request, "myapp/setting.html")

@login_required
def username_change(request):
    user = request.user
    obj = User.objects.get(id= user.id)
    form = UsernameForm()
    if request.method == 'POST':
        username = UsernameForm(request.POST,instance = obj)
        if username.is_valid:
            username.save()
            return render(request,'myapp/change_complete.html',{'item':'ユーザー名'})
    
    return render(request,'myapp/change.html',{'item':'ユーザー名','form':form})

@login_required
def mail_change(request):
    user = request.user
    obj = User.objects.get(id= user.id)
    form = MailForm()
    if request.method == 'POST':
        email = MailForm(request.POST,instance = obj)
        if email.is_valid:
            email.save()
            return render(request,'myapp/change_complete.html',{'item':'メールアドレス'})
    
    return render(request,'myapp/change.html',{'item':'メールアドレス','form':form})
    
class UserUpdateView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = UpdateForm
    template_name = 'myapp/setting2.html'
    success_url = reverse_lazy('change_complete')



class password_change(LoginRequiredMixin,PasswordChangeView):
    form_class = PasswordForm
    template_name = 'myapp/password_change.html'
    success_url = reverse_lazy('setting')


class logout_view(LoginRequiredMixin,LogoutView):
    template_name = 'myapp/index.html'