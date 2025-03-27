from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from .forms import SignUpForm, LoginForm
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from .models import Talk
from django.db.models import Q

CustomUser = get_user_model()

def index(request):
    return render(request, "myapp/index.html")

class SignUpView(CreateView):
    
    model = CustomUser
    form_class = SignUpForm
    template_name = "myapp/signup.html"
    success_url = reverse_lazy("myapp:index")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return redirect(self.get_success_url())

class UserLogin(LoginView):
    template_name = 'myapp/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True
    
class UserLogout(LoginRequiredMixin, LogoutView):
    pass

class FriendsList(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'myapp/friends.html'
    context_object_name = 'users'
    
    def get_queryset(self):
        return CustomUser.objects.exclude(username=self.request.user.username)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_in_user =self.request.user
        users = context['users']
        
        
        user_and_latest_messages = []
        for user in users:
            latest_message = Talk.objects.filter(
            Q(sender=logged_in_user, receiver=user) | Q(sender=user, receiver=logged_in_user)).order_by('created_at').last()

            user_and_latest_messages.append({
                'user': user,
                'message': latest_message
            })


        context['user_and_latest_messages'] = user_and_latest_messages
        print(context['user_and_latest_messages'])
    
        

        return context
        
    

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
