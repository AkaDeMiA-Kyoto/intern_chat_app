from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view, name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('setting_username', views.setting_username, name='setting_username'),
    path('setting_mailaddress', views.setting_mailaddress, name='setting_mailaddress'),
    path('setting_icon', views.setting_icon, name='setting_icon'),
    path('setting_password', views.setting_password, name='setting_password'),
    path('setting_username_completed', views.setting_username_completed, name='setting_username_completed'),
    path('setting_mailaddress_completed', views.setting_mailaddress_completed, name='setting_mailaddress_completed'),
    path('setting_icon_completed', views.setting_icon_completed, name='setting_icon_completed'),
    path('setting_password_completed', views.setting_password_completed, name='setting_password_completed'),
]
