from django.urls import path, include
from . import views

app_name = "myapp"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<your_id>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path("change_setting/<change_command>/<your_id>", views.change_setting, name="change_setting"),
    path("change_setting_done/<change_command>", views.change_setting_done, name="change_setting_done"),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
]
