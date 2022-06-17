from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static
from myapp.models import CustomUser


urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.Signup.as_view(), name='signup_view'),
    path('login', views.Login.as_view(), name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:Customuser_id>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('',views.Logout.as_view(),name='logout'),
    path('passwordchange',views.PasswordChange.as_view(),name='passwordchange'),
    path('username_change',views.UsernameChange.as_view(),name='username_change'),
    path('icon_change',views.IconChange.as_view(),name='icon_change'),
    path('adress_change',views.AdressChange.as_view(),name='adress_change'),
]
