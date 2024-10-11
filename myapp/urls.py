from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view, name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:user_id>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('setting_username', views.setting_username, name='setting_username'),
    path('setting_adress', views.setting_adress, name='setting_adress'),
    path('setting_image', views.setting_image, name='setting_image'),
    path('setting_password', views.setting_password, name='setting_password'), 
    path('user_logout' ,views.user_logout, name='user_logout'),
    path('mail_test/', views.users_mail_test, name='mail_test'),
]