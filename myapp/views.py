from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages  
from django.contrib.auth import login,authenticate,get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView,UpdateView
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView
from .forms import SignUpForm, LogInForm,ChangeImageForm,ChatMessageForm
from .models import CustomUser,ChatMessage
from django.db.models import Q
class IndexView(TemplateView):
    template_name = "myapp/index.html"

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'myapp/signup.html'
    success_url = reverse_lazy("myapp:index")
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    def form_invalid(self,form):
        messages.error(self.request,'失敗しました') 
        return super().form_invalid(form)   
class CustomLoginView(LoginView):
    form_class = LogInForm
    template_name = 'myapp/login.html'
    #LoginViewのsuccess_urlはデフォルトで定義されてないので、settings.pyに記述

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

@login_required
def friends(request):
    people = CustomUser.objects.all().order_by('-date_joined')
    #ChatMessageから相手がsenderとして送られたメッセージから、最新の時刻とメッセージのみを取得
    me = request.user
    admin = CustomUser.objects.get(username = 'admin')
    not_friends_data =[]
    friends_data=[]
    for person in people:
        if person != me and person != admin: 
            last_message = ChatMessage.objects.filter(sender=person,receiver = me ).order_by('created_at').last()
            if last_message :
                friends_data.append( {
                    "user": person,
                    "message": last_message.message,
                    "time": last_message.created_at,
                })
            else:
                not_friends_data.append( {
                    "user": person,
                    "message": None,
                    "time": person.date_joined,
                })
            people_data =  friends_data + not_friends_data
            context = {'people_data':people_data}
    return render(request, "myapp/friends.html",context)

@login_required    
def setting(request):
    return render(request, "myapp/setting.html")
class ChangeUsernameView(UpdateView,LoginRequiredMixin):
    model = CustomUser
    fields = ['username']
    template_name = 'myapp/setting/username.html'
    success_url = reverse_lazy('myapp:setting')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        # ユーザー名の変更前にバリデーションを行う
        new_username = form.cleaned_data['username']
        if CustomUser.objects.filter(username=new_username).exists():
            form.add_error('username', '既に使用されているユーザー名です。')
            return self.form_invalid(form)
        return super().form_valid(form)
    def form_invalid(self,form):
        messages.error(self.request,'失敗しました') 
        return super().form_invalid(form)   
    

class ChangeEmailView(UpdateView,LoginRequiredMixin):
    model = CustomUser
    fields = ['email']
    template_name = 'myapp/setting/email.html'
    success_url = reverse_lazy('myapp:setting')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        # ユーザー名の変更前にバリデーションを行う
        new_username = form.cleaned_data['email']
        if CustomUser.objects.filter(username=new_username).exists():
            form.add_error('email', '既に使用されているメールアドレスです。')
            return self.form_invalid(form)
        return super().form_valid(form)
    def form_invalid(self,form):
        messages.error(self.request,'失敗しました') 
        return super().form_invalid(form)   

class ChangePasswordView(PasswordChangeView,LoginRequiredMixin):
    model = CustomUser
    template_name = 'myapp/setting/password.html'
    success_url = reverse_lazy('myapp:setting')
    def get_success_url(self):
        return reverse_lazy('myapp:setting')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        return super().form_valid(form)
    def form_invalid(self,form):
        messages.error(self.request,'失敗しました') 
        return super().form_invalid(form)   
    
class ChangeImageView(UpdateView,LoginRequiredMixin):
    model = CustomUser
    form_class = ChangeImageForm
    template_name = 'myapp/setting/image.html'
    success_url = reverse_lazy('myapp:setting')
    def get_object(self):
        return self.request.user
    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)
    def form_invalid(self,form):
        messages.error(self.request,'失敗しました') 
        return super().form_invalid(form)   

@login_required    
def talk_room(request,username):
    user = request.user
    if username == user.username:
        return redirect("/setting")
    sender = CustomUser.objects.get(username=request.user.username) # 自分のcustomUserもでる
    receiver = CustomUser.objects.get(username=username) #相手のcustomUserもでる
    messages = ChatMessage.objects.filter(Q(sender= sender,receiver=receiver) | Q(sender= receiver,receiver=sender)).order_by('created_at')
    
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            ChatMessage.objects.create(
                sender=sender,
                receiver=receiver,
                message=form.cleaned_data['message'],
            )
            
    else:
        form = ChatMessageForm()

    context = {
        'sender':sender,
        'receiver': receiver,
        'messages': messages,
        'form': form,
    }
    return render(request, 'myapp/talk_room.html', context)


