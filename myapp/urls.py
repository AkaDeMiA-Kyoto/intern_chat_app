from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.SignupView.as_view(), name='signup_view'),
    path('login', views.Login.as_view(), name='login_view'),
    path('friends', views.FriendsView.as_view(), name='friends'),
    path('talk_room/<int:id>', views.TalkView.as_view(), name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('username_update/<int:pk>', views.UsernameUpdateView.as_view(), name='username_update'),
    path('username_update_complete', views.username_update_complete, name='username_update_complete'),
    path('email_update/<int:pk>', views.EmailUpdateView.as_view(), name='email_update'),
    path('email_update_complete', views.email_update_complete, name='email_update_complete'),
    path('password_update/<int:pk>', views.PasswordUpdateView.as_view(), name='password_update'),
    path('password_update_complete', views.password_update_complete, name='password_update_complete'),
    path('icon_update/<int:pk>', views.IconUpdateView.as_view(), name='icon_update'),
    path('icon_update_complete', views.icon_update_complete, name='icon_update_complete')
]