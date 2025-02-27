from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.ChatLoginView.as_view(), name='login'), #classの呼び出しにはas_view()メソッド必要。
    path('friends/', views.getFriendsList, name='friends'),
    path('talk_room/', views.talk_room, name='talk_room'),
    path('setting/', views.setting, name='setting'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
