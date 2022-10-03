from django.urls import path
from . import views


app_name = 'myapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('friends/', views.friends, name='friends'),
    path('talk_room/<int:friend_id>/', views.talk_room, name='talk_room'),
    path('setting/', views.setting, name='setting'),
    path('name_change/', views.name_change, name='name_change'),
    path('email_add/', views.email_add, name='email_add'),
    path('icon_change/', views.icon_change, name='icon_change'),
]
