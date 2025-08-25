from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from .forms import SignUpForm ,LoginForm
from django.db.models import Q, OuterRef, Subquery, Case, When, IntegerField
from .models import Message
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect

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

def talk_room(request):
    me = request.user
    partner = get_object_or_404(User, pk=user_id)
    if partner.pk == me.pk:
        return redirect('home')

    qs = Message.objects.filter(
        Q(sender=me, receiver=partner) | Q(sender=partner, receiver=me)
    ).select_related('sender', 'receiver').order_by('created_at')  # 古い→新しい

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(sender=me, receiver=partner, content=content)
            return redirect('talk_room', user_id=partner.pk)

    return render(request, 'myapp/talk_room.html', {'partner': partner, 'messages': qs})

def setting(request):
    return render(request, "myapp/setting.html")
