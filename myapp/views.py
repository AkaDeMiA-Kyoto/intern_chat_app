from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, ListView
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from . import forms
from .forms import SingupForm, LoginForm

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    form = forms.SingupForm()
    return render(request, "myapp/signup.html", {'form': form})

def login_view(request):
    return render(request, "myapp/login.html")

def setting(request):
    return render(request, "myapp/setting.html")

def register(request):
    if request.method == 'POST':
        form = SingupForm(request.POST,request.FILES)
        if form.is_valid():
            print('ok')
            # ユーザー登録
            CustomUser.objects.create(
                username=request.POST['username'], 
                email=request.POST['email'], 
                password=make_password(request.POST['password']), 
                icon_image=request.FILES['image']
                )
            return redirect('index')
        else:
            print('is not ok')
            answer = form
            form = SingupForm()
            context = {
                'form' : form,
                'answer' : answer
            }
            return render(request, "myapp/signup.html", context)

# 参考
# https://kamatimaru.hatenablog.com/entry/2020/05/12/060236

# https://marsquai.com/745ca65e-e38b-4a8e-8d59-55421be50f7e/05f253f8-c11b-4c91-8091-989eb2600a7b/de4d464b-1e55-47f4-b993-85dad837dcab/

class Login(LoginView):
    form_class = LoginForm
    template_name = 'myapp/login.html'

class Friends(LoginRequiredMixin, TemplateView):
    template_name = 'myapp/friends.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        friends = CustomUser.objects.exclude(id=1).exclude(id=user.id)
        context["friends"] = friends
        return context

    # 参考

    # https://office54.net/python/django/orm-database-operate

def talk_room(request, user_id, friend_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    friend = get_object_or_404(CustomUser, pk=friend_id)
    context = {'user': user, 'friend' : friend}
    return render(request, "myapp/talk_room.html", context)


# class Friends(LoginRequiredMixin, ListView):
#     template_name = 'myapp/friends.html'
#     model = CustomUser

# def friends(request, pk):
#     user = CustomUser.objects.get(pk=pk)
#     friends = CustomUser.objects.all()
#     context = {'user':user, 'friends': friends}
#     return render(request, "myapp/friends.html", context)

# class Talk_room(LoginRequiredMixin, TemplateView):
#     template_name = 'myapp/talk_room.html'
    
