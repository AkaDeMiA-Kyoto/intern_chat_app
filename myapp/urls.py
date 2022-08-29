from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup'),
    path('login', views.login_view.as_view(), name='login'),
    path('friends', views.friends, name='friends'),
    path('talk_room', views.talk_room, name='talkroom'),
    path('setting', views.setting, name='setting'),
]
