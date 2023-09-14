from django.shortcuts import redirect, render, get_object_or_404
from .forms import SignUpForm
from .forms import LoginForm
from django.contrib.auth.views import LoginView
from .models import CustomUser
from .forms import TalkForm
from .models import Talk
from django.db.models import Q

def setting(request):
    return render(request, "myapp/base.html") #新しく追加したやつ

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == "GET":
        form = SignUpForm()
        context = {
            "form": form,
        }
        return render(request, "myapp/signup.html", context)
    
    elif request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("index")
        else:
            context = {
                "form": form,
            }
            return render(request, "myapp/signup.html", context)
    
    return redirect("index")

class Login(LoginView):
    template_name = "myapp/login.html"
    authentication_form = LoginForm

def friends(request):
    data = CustomUser.objects.all().order_by('date_joined')
    context = { 
        "data": data
    }
    return render(request, "myapp/friends.html", context)

def talk_room(request, id):
    user = request.user
    friendname = get_object_or_404(CustomUser, pk=id)
    talk = Talk.objects.filter(
        Q(talk_from = user, talk_to = friendname) | Q(talk_from = friendname, talk_to = user)
    )
    context = {
        "friendname": friendname,
        "form": TalkForm(),
        "talk": talk,
    }

    if request.method == "POST":
        obj = Talk()
        form = TalkForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(to='/talk_room')
        
    return render(request, "myapp/talk_room.html", context)

def setting(request):
    return render(request, "myapp/setting.html")


