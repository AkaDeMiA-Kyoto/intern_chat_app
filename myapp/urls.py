from django.urls import path
from . import views


app_name = 'myapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('friends/', views.friends, name='friends'),
    path('talk_room/<int:friend_id>/', views.talk_room, name='talk_room'),
    path('setting/', views.setting, name='setting'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('name_change/', views.name_change, name='name_change'),
    path('email_change/', views.email_change, name='email_change'),
    path('icon_change/', views.icon_change, name='icon_change'),
]
