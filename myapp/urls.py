from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .views import Logout, PasswordChange, login_view

app_name = 'myapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', login_view.as_view(), name='login'),
    path('friends/', views.friends, name='friends'),
    path('talk_room/<str:username>/', views.talk_room, name="talk_room"),
    path('setting', views.setting, name='setting'),
    path('username_change/', views.username_change, name='username_change'),
    path('username_change/done/', views.username_change_done, name='username_change_done'),
    path('email_change/', views.email_change, name='email_change'),
    path('email_change/done/', views.email_change_done, name='email_change_done'),
    path('icon_change/', views.icon_change, name='icon_change'),
    path('icon_change/done/', views.icon_change_done, name='icon_change_done'),
    path('password_change/', PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name="myapp:password_change_done.html"), name='password_change_done'),
    path('logout/', Logout.as_view(), name='logout')
]