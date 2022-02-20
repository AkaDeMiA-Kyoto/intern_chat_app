from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('login', views.LoginView.as_view(), name='login'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:user_id>/<int:friend_id>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('password_change',views.PasswordChangeView.as_view(),name='password_change'),
    path('logout',views.LogoutView.as_view(),name='logout'),
    path('update/<int:pk>',views.UserUpdateView.as_view(),name='update'),
    path('change_complete',views.change_complete,name='change_complete')
]
