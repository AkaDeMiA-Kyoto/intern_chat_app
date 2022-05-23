from django.urls import path
from . import views


app_name = 'myapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.MyLogin.as_view(), name='login'),
    path('logout/', views.MyLogout.as_view(), name='logout'),
    path('friends/', views.friends, name='friends'),
    path('talk_room/', views.talk_room, name='talk_room'),
    path('setting/', views.setting, name='setting'),
]
