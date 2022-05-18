from django.shortcuts import redirect, render
from .forms import SignUpForm, LoginForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    form=SignUpForm()
    if request.method == 'POST':
        form=SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            _username=request.POST['username']
            _password=request.POST['password1']
            _email=request.POST['email']
            #_prof_img=request.FILES['prof_img']
            CustomUser.objects.create(username=_username,password=_password,email=_email,
            #prof_img=_prof_img
            )
            return redirect('index')
        else:
            print("Form is not Valid!")
            for err in form.errors:
                print(err)
            return render(request, "myapp/signup.html",{'form':form})
        
    return render(request, "myapp/signup.html",{'form':form})



def friends(request):
    data=CustomUser.objects.all()
    params={
        'data':data,
    }
    return render(request, "myapp/friends.html",params)

def talk_room(request,name):
    dic={
        'name':name
    }
    return render(request, "myapp/talk_room.html",dic)

def setting(request):
    return render(request, "myapp/setting.html")

class MyLoginView(LoginView):
    form_class=LoginForm
    template_name="myapp/login.html"
