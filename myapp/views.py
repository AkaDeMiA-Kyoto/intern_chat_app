from django.shortcuts import redirect, render
from .models import CustomUser, Talk
from .forms import SignUpForm, LoginForm, MessageForm, NameForm, MailForm, ImageForm
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy

def index(request):
    return render(request, "myapp/index.html")

class login_view(LoginView,LoginRequiredMixin):
    form_class = LoginForm
    template_name = "myapp/login.html"

def friends(request):
    all = CustomUser.objects.all().order_by("date_joined")
    never_talked_id=[]
    never_talked_username=[]
    never_talked_image=[]
    never_talked_time=[]
    talked_id=[]
    talked_username=[]
    talked_image=[]
    talked_time=[]
    talked_message=[]
    for friend in all:
        if friend != request.user:
            talk = Talk.objects.filter(Q(recipient=request.user, sender=friend)|Q(recipient=friend, sender=request.user)).values("message").last()
            if talk==None:
                never_talked_id.append(friend.id)
                never_talked_username.append(friend.username)
                never_talked_image.append(friend.image)
                never_talked_time.append(friend.date_joined) 
            else:
                time=Talk.objects.filter(Q(recipient=request.user, sender=friend)|Q(recipient=friend, sender=request.user)).values("arrived_at").last()
                talked_id.append(friend.id)
                talked_username.append(friend.username)
                talked_image.append(friend.image)
                talked_time.append(time)
                talked_message.append(talk)
    zipped_never_data = zip(never_talked_id, never_talked_username, never_talked_image, never_talked_time)
    zipped_data=zip(talked_id,talked_username,talked_image,talked_time,talked_message)
    zipped_data=sorted(zipped_data, key=lambda x:x[3])
    params={
        "zipped_never_data":zipped_never_data,
        "zipped_data":zipped_data
    }
    return render(request,"myapp/friends.html",params)

def talk_room(request,user_id):
    if request.method=='POST':
        message=request.POST["message"]
        from_user=request.user
        to_user=CustomUser.objects.get(id=user_id)
        Talk.objects.create(
            sender=from_user,
            recipient=to_user,
            message=message
        )
        return redirect(talk_room,user_id=to_user.id)
    else:
        user=CustomUser.objects.get(id=user_id)
        msgs = Talk.objects.filter(Q(recipient=request.user, sender=user)|Q(recipient=user, sender=request.user)).order_by("arrived_at")
        params={
            "opponent":user,
            "user_id":user_id,
            "himself":request.user,
            "form":MessageForm(),
            "msgs":msgs
        }
        return render(request,"myapp/talk_room.html",params)

def setting(request):
    return render(request, "myapp/setting.html")

def signup_view(request):
    if request.method=='POST':
        form = SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = SignUpForm()

    return render(request,"myapp/signup.html",{'form':form})

def n_done(request):
    return render(request,"myapp/n_done.html")

def m_done(request):
    return render(request,"myapp/m_done.html")

def i_done(request):
    return render(request,"myapp/i_done.html")


def p_done(request):
    return render(request,"myapp/p_done.html")

class password_change(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('p_done.html')
    template_name = 'myapp/password_change.html'

def username_change(request):
    if request.method == 'POST':
        u=request.user
        a=request.POST["a"]
        u.name=a
        u.save()
        return redirect(request,"myapp/n_done.html")
    else:
        form=NameForm()
        return render(request,"myapp/username_change.html",{"form":form})

def mail_change(request):
    if request.method == 'POST':
        u=request.user
        a=request.POST["a"]
        u.name=a
        u.save()
        return redirect(request,"myapp/m_done.html")
    else:
        form=MailForm()
        return render(request,"myapp/mail_change.html",{"form":form})

def image_change(request):
    if request.method == 'POST':
        u=request.user
        a=request.POST["a"]
        u.name=a
        u.save()
        return redirect(request,"myapp/i_done.html")
    else:
        form=ImageForm()
        return render(request,"myapp/image_change.html",{"form":form})
    
class logout(LogoutView):
    template_name = 'setting.html'