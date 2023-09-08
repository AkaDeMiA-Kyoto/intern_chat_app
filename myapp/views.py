from django.shortcuts import redirect, render
from django.views.generic import CreateView,ListView
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from myapp.models import CustomUser, Chat
from .forms import SignupForm,CustomLoginForm,CustomNameChangeForm,CustomAddressChangeForm,CustomIconChangeForm
from django.urls import reverse_lazy

class SignupView(CreateView):
    template_name="myapp/signup.html"
    form_class=SignupForm
    redirect_url="index"
    
class CustomLoginView(LoginView):
    template_name='myapp/login.html'
    authentication_form=CustomLoginForm
    #redirect_url="friend"
    
class CustomLogoutView(LogoutView):
    template_name='myapp/index.html'

class CustomListView(ListView):
    template_name='myapp/friends.html'
    queryset=CustomUser.objects.order_by('date_joined')



def index(request):
    return render(request, "myapp/index.html")

def talk_room(request, friend_id):
    friend = CustomUser.objects.get(id=friend_id)
    chats = Chat.objects.filter(Q(send_from=friend) | Q(send_to=friend)).order_by('created_at')
    context = {
        'friend': friend,
        'chats': chats,  
        'user': request.user,  
    }
    
    if request.method == "POST":
        data = request.POST
        # {'content': '文章'}
        content = data.get('content')
        send_from = request.user
        send_to = friend
        
        # 送信内容を取得して、それを保存する
        chat = Chat.objects.create(
            content=content,
            send_from=send_from,
            send_to=send_to,
        )
        chat.save()
    return render(request, "myapp/talk_room.html", context)

def setting(request):
    return render(request, "myapp/setting.html")

def change_name(request):
    if request.method == 'POST':
        form = CustomNameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('setting')
    else:
        form = CustomNameChangeForm()
    return render(request, 'myapp/change_name.html',{'form':form})
    
def change_address(request):
    if request.method == 'POST':
        form = CustomAddressChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('setting')
    else:
        form = CustomAddressChangeForm()
    return render(request, 'myapp/change_address.html',{'form':form})

def change_icon(request):
    if request.method == 'POST':
        form = CustomIconChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('setting')
    else:
        form = CustomIconChangeForm()
    return render(request, 'myapp/change_icon.html',{'form':form})

class ChangePassword(LoginRequiredMixin,PasswordChangeView):
    success_url = reverse_lazy('setting')
    template_name = 'myapp/change_password.html'
    
    