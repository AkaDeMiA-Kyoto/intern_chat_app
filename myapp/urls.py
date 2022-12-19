from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup'),
    path('login', views.MyLogin.as_view(), name='login'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<str:username>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
]
