from django.urls import path
from . import views
app_name = 'myapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup_view'),
    path('login/', views.UserLogin.as_view(), name='login_view'),
    path('friends/', views.friends, name='friends'),
    path('talk_room/<int:user_id>/', views.talk_room, name='talk_room'),
    path('setting/', views.setting, name='setting'),
    path('setting/name/',  views.setting_name,  name='setting_name'),
    path('setting/email/', views.setting_email, name='setting_email'),
    path('setting/icon/',  views.setting_icon,  name='setting_icon'),
    path('setting/password/', views.PasswordChange.as_view(), name='setting_password'),
    path('setting/password/done/', views.setting_password_done, name='setting_password_done'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
]
