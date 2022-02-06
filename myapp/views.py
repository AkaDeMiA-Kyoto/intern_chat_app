from django.shortcuts import redirect, render
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Profile
from .models import Message
from .forms import UserChangeForm,UserPasswordChangeForm
from .forms import MessageForm
from .forms import SignUpForm
from .forms import LoginForm


class Index(TemplateView):
    template_name = "myapp/index.html"
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['goto_signup'] = 'account_signup'
        context['goto_login'] = 'account_login'
        return context

@login_required
def friends(request):
    user=request.user
    friends=[]
    never_talked_friends=[]
    data = Profile.objects.exclude(id=user.id)
    for friend in data:
        latests = Message.objects.all().filter(Q(sender=request.user) | Q(receiver=request.user)).filter(Q(sender=friend) | Q(receiver=friend)).order_by('created_at').last()
        if latests != None:
            friends.append([friend,latests])
        else:
            never_talked_friends.append(friend)
   
    params = {
        'user':user,
        'data':data,
        'never_talked_friends':never_talked_friends,
        'friends':friends,
    }
    return render(request, "myapp/friends.html",params)

@login_required
def talk_room(request,username):
    user=request.user
    if request.method=='POST':
        obj=Message()
        message=MessageForm(request.POST,instance=obj)
        if message.is_valid():
            obj.receiver=Profile.objects.get(username=username)
            obj.sender=Profile.objects.get(username=user)
            content=message.cleaned_data.get("content")
            message.save()
    else:
        message=MessageForm()
    data=Message.objects.all().reverse()
    receiver=Profile.objects.get(username=username)
    params={
        'receiver':receiver,
        'user':user,
        'data':data,
        'message':message,
    }
    return render(request, "myapp/talk_room.html",params)

def setting(request):
    user=request.user
    params={
        'user':user
    }
    return render(request, "myapp/setting.html",params)

@login_required
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Login'))

@login_required
def update_username(request):
    if(request.method=="POST"):
        form=UserChangeForm(request.POST)
        if(form.is_valid):
            new_username=request.POST['username']
            old_obj=Profile.objects.get(username=request.user.username)
            old_obj.username=new_username
            old_obj.save()
            return redirect('update_username_complete')
    else:
        form=UserChangeForm()
    params={
        'form':form
    }
    return render(request, "myapp/update_username.html",params)

@login_required
def update_username_complete(request):
    return render(request, "myapp/update_username_complete.html")

@login_required
def update_email(request):
    if(request.method=="POST"):
        form=UserChangeForm(request.POST)
        if(form.is_valid):
            new_email=request.POST['email']
            old_obj=Profile.objects.get(username=request.user.username)
            old_obj.email=new_email
            old_obj.save()
            return redirect('update_email_complete')
    else:
        form=UserChangeForm()
    params={
        'form':form
    }
    return render(request, "myapp/update_email.html",params)

@login_required
def update_email_complete(request):
    return render(request, "myapp/update_email_complete.html")

@login_required
def update_image(request):
    if(request.method=="POST"):
        form=UserChangeForm(request.FILES)
        if(form.is_valid):
            new_image=request.FILES['image']
            old_obj=Profile.objects.get(username=request.user.username)
            old_obj.image=new_image
            old_obj.save()
            return redirect('update_image_complete')
    else:
        form=UserChangeForm()
    params={
        'form':form
    }
    return render(request, "myapp/update_image.html",params)

@login_required
def update_image_complete(request):
    return render(request, "myapp/update_image_complete.html")

@login_required
def update_password(request):
    form=UserPasswordChangeForm(request.user,request.POST)
    if(request.method=='POST' and form.is_valid()):
        form.save()
        return redirect('login_view')
    
    params={
        'form':form,
    }
    return render(request, "myapp/update_password.html",params)

@login_required
def update_password_complete(request):
    return render(request, "myapp/update_password_complete.html")
