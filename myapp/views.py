from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from .forms import SignUpForm, LoginForm, SettingForm
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import CreateView, ListView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from .models import Talk
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

CustomUser = get_user_model()


def index(request):
    return render(request, "myapp/index.html")


class SignUpView(CreateView):

    model = CustomUser
    form_class = SignUpForm
    template_name = "myapp/signup.html"
    success_url = reverse_lazy("index")

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
        logged_in_user = self.request.user
        users = context['users']

        user_and_latest_messages = []
        for user in users:
            latest_message = Talk.objects.filter(
                Q(sender=logged_in_user, receiver=user) | Q(sender=user, receiver=logged_in_user)).order_by('created_at').last()

            user_and_latest_messages.append({
                'user': user,
                'message': latest_message.message if latest_message else None,
                'time': latest_message.created_at if latest_message else None,
            })
            

        context['user_and_latest_messages'] = user_and_latest_messages

        return context


class TalkRoomView(LoginRequiredMixin, TemplateView):
    template_name = 'myapp/talk_room.html'

    def get_queryset(self):
        other_user = get_object_or_404(CustomUser, id=self.kwargs['pk'])
        logged_in_user = self.request.user

        messages = Talk.objects.filter(
            Q(sender=logged_in_user, receiver=other_user) | Q(
                sender=other_user, receiver=logged_in_user)
        ).order_by('created_at')
        return messages

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = self.get_queryset()
        context['other_user'] = get_object_or_404(CustomUser, id=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        other_user = get_object_or_404(CustomUser, id=self.kwargs['pk'])
        message = request.POST.get('message')

        if message:
            Talk.objects.create(
                sender = request.user,
                receiver = other_user,
                message = message
            )
            return HttpResponseRedirect(reverse('talk_room', kwargs={'pk': other_user.pk}))

        return self.get(request, *args, **kwargs)


@login_required
def setting(request):
    return render(request, "myapp/setting.html")

class UsernameChangeView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = SettingForm
    template_name = 'myapp/username_change.html'
    success_url = reverse_lazy('username_change_done')

    def get_object(self):
        return self.request.user
    
@login_required
def username_change_done(request):
    return render(request, "myapp/username_change_done.html")

class MailChangeView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = SettingForm
    template_name = 'myapp/mail_change.html'
    success_url = reverse_lazy('mail_change_done')

    def get_object(self):
        return self.request.user
    
@login_required
def mail_change_done(request):
    return render(request, "myapp/mail_change_done.html")

class UserImgChangeView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = SettingForm
    template_name = 'myapp/user_img_change.html'
    success_url = reverse_lazy('user_img_change_done')

    def get_object(self):
        return self.request.user
    
@login_required
def user_img_change_done(request):
    return render(request, "myapp/user_img_change_done.html")

class MyPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'myapp/password_change.html'
    success_url = reverse_lazy('password_change_done')
    
class MyPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'myapp/password_change_done.html'

