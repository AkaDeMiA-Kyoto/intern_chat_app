from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render, get_object_or_404

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.models import Q, OuterRef, Subquery, Count
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from .forms import SignupForm, LoginForm, MessageForm, ChangeUsernameForm, ChangeEmailForm, ChangeImageForm, CustomPasswordChangeForm
from .models import Message
from accounts.models import CustomUser


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


@login_required
def friends(request):
    user = request.user
    query = request.GET.get('q')

    friends = CustomUser.objects.exclude(id=user.id).annotate(
        message_count=Count('message_from', filter=Q(message_from__message_to=user)) + Count('message_to', filter=Q(message_to__message_from=user))
    )

    if query:
        friends = friends.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query)
        ).distinct()

    # メッセージがあるユーザー
    friends_with_msg = friends.filter(
        ~Q(message_count=0)
    )

    # サブクエリ
    latest_msg = Message.objects.filter(
        Q(message_from=OuterRef("pk"), message_to=user) |
        Q(message_from=user, message_to=OuterRef("pk"))
    ).order_by("-time")

    friends_with_msg = friends_with_msg.annotate(
        latest_msg_talk=Subquery(latest_msg[:1].values("talk")),
        latest_msg_time=Subquery(latest_msg[:1].values("time"))
    ).values("id", "username", "image", "latest_msg_talk", "latest_msg_time").order_by("-latest_msg_time")

    # メッセージがないユーザー
    friends_without_msg = friends.filter(
        message_count=0
    ).values("id", "username", "image")

    context = {
        "friends_with_msg": friends_with_msg,
        "friends_without_msg": friends_without_msg,
        "query": query
    }
    return render(request, "myapp/friends.html", context)


@login_required
def talk_room(request, friend_id):
    user = request.user
    friend = get_object_or_404(CustomUser, pk=friend_id)
    messages = Message.objects.filter(
        Q(message_from=user, message_to=friend) |
        Q(message_from=friend, message_to=user)
    ).order_by("time")
    if request.POST:
        form = MessageForm(request.POST)
        if form.is_valid():
            Message.objects.create(
                message_from=user,
                message_to=friend,
                talk=form.cleaned_data['talk'],
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
