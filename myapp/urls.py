from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view.as_view(), name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:pk>/', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('logout/', auth_view.LogoutView.as_view() , name='logout'),
    path('change_username', views.change_username, name='change_username'),
    path('change_email', views.change_email, name='change_email'),
    path('change_icon', views.change_icon, name='change_icon'),
    path("accounts/password_change_form", auth_view.PasswordChangeView.as_view(template_name="myapp/change_password.html"), name="password_change_form"),
    path("accounts/password_change_done", auth_view.PasswordChangeDoneView.as_view(template_name="myapp/complete_password.html"), name="password_change_done"),
    path('complete_username', views.complete_username, name='complete_username'),
    path('complete_email', views.complete_email, name='complete_email'),
    path('complete_icon', views.complete_icon, name='complete_icon'),
]
