from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.LoginView.as_view(), name='login_view'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<user_id>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('setting_username', views.setting_username, name='setting_username'),
    path('setting_mailaddress', views.setting_mailaddress, name='setting_mailaddress'),
    path('setting_icon', views.setting_icon, name='setting_icon'),
    path('setting_password', views.PasswordChangeView.as_view(), name='setting_password'),
    path('setting_username_completed', views.setting_username_completed, name='setting_username_completed'),
    path('setting_mailaddress_completed', views.setting_mailaddress_completed, name='setting_mailaddress_completed'),
    path('setting_icon_completed', views.setting_icon_completed, name='setting_icon_completed'),
    path('setting_password_completed', views.PasswordChangeDoneView.as_view(), name='setting_password_completed'),
]
