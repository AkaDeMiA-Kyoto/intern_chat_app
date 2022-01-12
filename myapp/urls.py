from django.urls import path
from . import views

app_name = "myapp"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('friends', views.FriendsView.as_view(), name='friends'),
    path('talk_room/<int:your_id>', views.TalkRoomView.as_view(), name='talk_room'),
    path('setting', views.SettingView.as_view(), name='setting'),
    path("change_username", views.ChangeUsernameView.as_view(), name="change_username"),
    path("change_email", views.ChangeEmailView.as_view(), name="change_email"),
    path("change_image", views.ChangeImageView.as_view(), name="change_image"),
    path("change_setting_done/<str:change_command>", views.ChangeSettingDoneView.as_view(), name="change_setting_done"),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change_done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
]
