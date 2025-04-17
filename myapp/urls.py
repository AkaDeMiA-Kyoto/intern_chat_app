from django.urls import path
from . import views

app_name = "myapp"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signup', views.SignUpView.as_view(), name='signup_view'),
    path('login', views.CustomLoginView.as_view(), name='login_view'),
    path('logout', views.LogoutView.as_view(), name='logout_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<str:username>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('setting/username', views.ChangeUsernameView.as_view(), name='setting_username'),
    path('setting/email', views.ChangeEmailView.as_view(), name='setting_email'),
    path('setting/password', views.ChangePasswordView.as_view(), name='setting_password'),
    path('setting/image', views.ChangeImageView.as_view(), name='setting_image'),
]

