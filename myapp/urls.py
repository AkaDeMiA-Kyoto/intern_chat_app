from django.urls import path
from django.conf.urls import url
from .views import HelloView
from . import views

urlpatterns = [
    url('signup', HelloView.as_view(), name='signup_view'),
    path('', views.index, name='index'),
    path('login', views.login_view, name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
]
