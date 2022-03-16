from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignUpForm,TalkForm,PasswordForm,UpdateForm,SearchForm
from django.contrib.auth.views import LoginView,PasswordChangeView,LogoutView
from .models import TalkModel,User
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,UpdateView





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


class LoginView(LoginView):
    authentication_form = LoginForm
    template_name = "myapp/login.html"
    success_url = reverse_lazy('friends')


@login_required
def friends(request):
    login_user = request.user
    data = User.objects.exclude(id=login_user.id)
    if "word" in request.GET:
        word = request.GET['word']
        data = User.objects.filter(username__contains=word).exclude(id=login_user.id)


    params = {'data':data,'login_user':login_user,'form':SearchForm}
    return render(request, 'myapp/friends.html', params)


@login_required
def talk_room(request,user_id,friend_id):
    if user_id != request.user.id:
        raise Http404
    user = User.objects.get(id=user_id)
    friend = User.objects.get(id=friend_id)
    talks = TalkModel.objects.filter(Q(sender=user, talkname=friend) | Q(sender=friend, talkname=user))
    talkform = TalkForm()
    params = {'friend':friend,'talks':talks,'form':talkform}
    
    '''if request.method == 'POST':
        talkform = TalkForm(request.POST)
        if talkform.is_valid:
            talkform.instance.sender = user
            talkform.instance.talkname = friend
            talkform.save()
            print(talkform.instance.content)
        return redirect('talk_room',user_id,friend_id)'''

    return render(request,'myapp/talk_room.html',params)


@login_required
def setting(request):
    return render(request, "myapp/setting.html")

    
class UserUpdateView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = UpdateForm
    template_name = 'myapp/update.html'
    success_url = reverse_lazy('change_complete')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object != request.user:
            raise Http404
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object != request.user:
            raise Http404
        return super().post(request, *args, **kwargs)


def change_complete(request):
    return render(request,'myapp/change_complete.html')


class PasswordChangeView(LoginRequiredMixin,PasswordChangeView):
    form_class = PasswordForm
    template_name = 'myapp/password_change.html'
    success_url = reverse_lazy('setting')


class LogoutView(LoginRequiredMixin,LogoutView):
    template_name = 'myapp/index.html'