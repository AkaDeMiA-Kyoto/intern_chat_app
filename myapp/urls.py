from django.urls import path
from . import views

app_name = "myapp"
urlpatterns = [
    path('', views.index, name='index'),
    path('base', views.base, name='base'),
    path('signup', views.signup_view, name='signup'),
    path('login', views.Login.as_view(), name='login'),
    path('friends', views.Friends.as_view(), name='friends'),
    path('talk_room/<int:user_id>/<int:friend_id>', views.talk_room, name='talk_room'),
    path('send_message', views.send_message, name='send_message'),
    path('setting', views.setting, name='setting'),
    path('register', views.register, name='register'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('password_change', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('name_change', views.NameChange.as_view(), name='name_change'),
    path('email_change', views.EmailChange.as_view(), name='email_change'),
    path('icon_change', views.IconChange.as_view(), name='icon_change'),
    path('inf_change_done', views.InfChangeDone.as_view(), name='inf_change_done')
]

