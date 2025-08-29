from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.shortcuts import redirect, render
from .forms import SignUpForm ,LoginForm
from django.db.models import Q, OuterRef, Subquery, Case, When, IntegerField
from .models import Message
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy

from .forms import NameForm, EmailForm, IconForm

User = get_user_model()

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == "GET":
        form = SignUpForm()
    elif request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect("/")

        else:
            print(form.errors)
    context = {"form": form}
    return render(request, "myapp/signup.html", context)

class UserLogin(LoginView):
    form_class = LoginForm
    template_name = "myapp/login.html"

@login_required
def friends(request):
    me = request.user
    others = User.objects.exclude(pk=me.pk)
    last_qs = Message.objects.filter(
        Q(sender=me, receiver=OuterRef('pk')) | Q(sender=OuterRef('pk'), receiver=me)
    ).order_by('-created_at')

    others = others.annotate(
        last_message=Subquery(last_qs.values('content')[:1]),
        last_time   =Subquery(last_qs.values('created_at')[:1]),
    ).annotate(
        has_chat=Case(
            When(last_time__isnull=False, then=1),
            default=0,
            output_field=IntegerField(),
        )
    ).order_by('-has_chat', '-last_time', '-date_joined')  # 仕様通りの並び順

    return render(request, 'myapp/friends.html', {'users': others})

@login_required
def talk_room(request, user_id: int):
    me = request.user
    partner = get_object_or_404(User, pk=user_id)
    if partner.pk == me.pk:
        return redirect('home')


    if request.method == 'POST':
        content = (request.POST.get('content') or '').strip()
        if content:
            Message.objects.create(sender=me, receiver=partner, content=content)
        return redirect(reverse('myapp:talk_room', args=[partner.pk]) + '#bottom')

    messages_qs = (
        Message.objects
        .filter(Q(sender=me, receiver=partner) | Q(sender=partner, receiver=me))
        .select_related('sender')
        .order_by('created_at')
    )

    ctx = {
        'partner': partner,
        'messages': messages_qs,
    }
    return render(request, 'myapp/talk_room.html', ctx)

@login_required
def setting(request):
    return render(request, "myapp/setting.html")

@login_required
def setting_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('myapp:setting')
    else:
        form = NameForm(instance=request.user)
    return render(request, 'myapp/setting/name.html', {'form': form})

@login_required
def setting_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('myapp:setting')
    else:
        form = EmailForm(instance=request.user)
    return render(request, 'myapp/setting/email.html', {'form': form})

@login_required
def setting_icon(request):
    if request.method == 'POST':
        form = IconForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('myapp:setting')
    else:
        form = IconForm(instance=request.user)
    return render(request, 'myapp/setting/icon.html', {'form': form})

class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    template_name = 'myapp/setting/password.html'
    success_url   = reverse_lazy('myapp:setting_password_done')

@login_required
def setting_password_done(request):
    return render(request, 'myapp/setting/password_done.html')

class UserLogout(LogoutView):
    next_page='myapp:index'