from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('login', views.UserLogin.as_view(), name='login'),
    path('logout', views.UserLogout.as_view(), name='logout'),
    path('friends', views.FriendsList.as_view(), name='friends'),
    path('talk_room/<int:pk>/', views.TalkRoomView.as_view(), name='talk_room'),
    path("setting", views.setting, name="setting"),
    path("username_change", views.UsernameChangeView.as_view(), name="username_change"),
    path("username_change_done/", views.username_change_done, name="username_change_done"),
    path("mail_change/", views.MailChangeView.as_view(), name="mail_change"),
    path("mail_change_done/", views.mail_change_done, name="mail_change_done"),
    path("user_img_change/", views.UserImgChangeView.as_view(), name="user_img_change"),
    path("user_img_change_done/", views.user_img_change_done, name="user_img_change_done"),
    path("password_change/", views.MyPasswordChangeView.as_view(), name="password_change"),
    path("password_change_done/", views.MyPasswordChangeDoneView.as_view(), name="password_change_done"),
]
