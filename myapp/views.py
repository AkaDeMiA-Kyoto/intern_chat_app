from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.shortcuts import render


class SignUp(generic.CreateView):

    form_class = CustomUserCreationForm
    success_url = reverse_lazy('chat:home')
    template_name = 'myapp/signup.html'

    def form_valid(self, form):
        """
        ユーザ登録直後に自動的にログオンさせる。
        self.objectにsave()されたユーザオブジェクトが格納されている。
        """
        valid = super().form_valid(form)
        login(self.request, self.object)   #login処理
        return valid
