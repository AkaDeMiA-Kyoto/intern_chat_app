from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.CreateAccount, name='signup_view'),
    path('login', views.Account_login.as_view(), name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:user_id>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('password',views.PasswordChange.as_view(),name='passwordchange'),
    path('passwordchange',views.PasswordChangeDone.as_view(),name='password_change_done'),
    path('logout',views.Logout.as_view() ,name='logout_view'),
    path('username_change',views.username_change,name='username_change'),
    path('username_change_done',views.username_change_done,name="username_change_done"),
    path('icon_change_done',views.icon_change,name="icon_change"),
    path('icon_change_done',views.icon_change_done,name="icon_change_done"),
    path('mailchange',views.email_change,name="email_change"),
    path('mail_change_done',views.email_change_done,name="email_change_done")
]
