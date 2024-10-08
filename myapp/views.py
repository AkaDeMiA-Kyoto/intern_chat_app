from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render, get_object_or_404

from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from .forms import SignupForm, LoginForm, MessageForm, ChangeUsernameForm, ChangeEmailForm, ChangeImageForm, CustomPasswordChangeForm
from .models import Message
from accounts.models import CustomUser


# def index(request):
#     return render(request, "myapp/index.html")

class IndexView(TemplateView):
    """ ホームビュー """
    template_name = "myapp/index.html"


def signup(request):
    if request.POST:
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('myapp:login')
    else:
        form = SignupForm()
    return render(request, "myapp/signup.html", {'form': form})


class UserSignupView(CreateView):
    """ ユーザー登録用ビュー """
    form_class = SignupForm
    template_name = "myapp/signup.html"
    success_url = reverse_lazy("myapp:signup")


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'myapp/login.html'
    redirect_field_name = REDIRECT_FIELD_NAME

    # def form_valid(self, form):
    #     form.instance.customuser_id = self.kwargs['customuser_pk']
    #     customuser = get_object_or_404(CustomUser, pk=)
    #     return redirect('myapp/friends', {'customuser': customuser})


"""
@login_required
def friends_bfr(request):
    user = request.user
    talk_info = []
    friends = CustomUser.objects.exclude(username=user.username)
    for friend in friends:
        latest_message = Message.objects.filter(
            Q(message_from=user, message_to=friend) |
            Q(message_from=friend, message_to=user)
        ).order_by("-sent_at").first()
        icon = friend.image
        if latest_message:
            talk_info.append(
                [
                    icon,
                    friend,
                    latest_message.message,
                    latest_message.sent_at
                ]
            )
        else:
            talk_info.append(
                [
                    icon,
                    friend,
                    None,
                    None
                ]
            )
        context = {
            'talk_info': talk_info
        }
    return render(request, "myapp/friends.html", context)
"""


@login_required
def friends(request):
    query = request.GET.get('q')
    user = request.user
    talk_info = []
    friends_no_talk = CustomUser.objects.exclude(username=request.user.username)
    if query:
        friends_no_talk = friends_no_talk.filter(
            Q(username=query)
        ).distinct()
    messages = Message.objects.filter(
        Q(message_from=user) |
        Q(message_to=user)
    ).order_by("-sent_at")
    for message in messages:
        if friends_no_talk.filter(
            Q(username=message.message_from) |
            Q(username=message.message_to)
        ).exists():
            friend = CustomUser.objects.filter(
                Q(username=message.message_from) |
                Q(username=message.message_to)
            ).exclude(username=user.username).get()
            talk_info.append(
                [
                    friend.image,
                    friend,
                    message,
                    message.sent_at
                ]
            )
            friends_no_talk = friends_no_talk.exclude(username=friend.username)
        else:
            continue

    for friend in friends_no_talk:
        talk_info.append(
            [
                friend.image,
                friend,
                None,
                None
            ]
        )

    context = {
        'talk_info': talk_info,
        'query': query,
    }
    return render(request, "myapp/friends.html", context)


@login_required
def talk_room(request, friend_id):
    user = request.user
    friend = get_object_or_404(CustomUser, pk=friend_id)
    messages = Message.objects.filter(
        Q(message_from=user, message_to=friend) |
        Q(message_from=friend, message_to=user)
    ).order_by("sent_at")
    if request.POST:
        form = MessageForm(request.POST)
        if form.is_valid():
            Message.objects.create(
                message_from=user,
                message_to=friend,
                message=form.cleaned_data['message'],
            )
            return redirect('myapp:talk_room', friend_id)
    else:
        form = MessageForm()

    context = {
        'friend': friend,
        'messages': messages,
        'form': form
    }
    return render(request, "myapp/talk_room.html", context)


@login_required
def setting(request):
    return render(request, "myapp/setting.html")


@login_required
def cha_name(request):
    user = request.user
    form = ChangeUsernameForm(request.POST or None)
    if form.is_valid():
        # user = CustomUser.objects.get(pk=user.id)
        user.username = form.cleaned_data['username_new']
        user.save()
        # render系の処理をする
        return redirect('myapp:cha_completed')

    context = {
        'form': form
    }

    return render(request, "myapp/cha_name.html", context)


@login_required
def cha_email(request):
    user = request.user
    form = ChangeEmailForm(request.POST or None)
    if form.is_valid():
        user.email = form.cleaned_data['email_new']
        user.save()
        return redirect('myapp:cha_completed')

    context = {
        'form': form
    }
    return render(request, "myapp/cha_email.html", context)


@login_required
def cha_image(request):
    user = request.user
    image = user.image
    form = ChangeImageForm(request.POST or None)
    if form.is_valid():
        if request.FILES.get('image_new'):
            user.image = request.FILES.get('image_new')
            user.save()
            return redirect('myapp:cha_completed')

    context = {
        'form': form,
        'image': image
    }

    return render(request, "myapp/cha_image.html", context)


@login_required
def cha_pass(request):
    return render(request, "myapp/cha_pass.html")


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('myapp:cha_done')
    template_name = 'myapp/cha_pass.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def cha_done(request):
    return render(request, "myapp/cha_done.html")
