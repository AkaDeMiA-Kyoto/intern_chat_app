from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view.as_view(), name='login_view'),
    path('friends', views.friends, name='friends'),
    path('setting', views.setting, name='setting'),
    path('talk_room/<int:user_id>/',views.talk_room,name='talk_room'),
    path('username_change',views.username_change,name='username_change'),
    path('mail_change',views.mail_change,name='mail_change'),
    path('image_change',views.image_change,name='image_change'),
    path('password_change',views.password_change.as_view(),name='password_change'),
    path('n_done',views.n_done,name='n_done'),
    path('m_done',views.m_done,name='m_done'),
    path('i_done',views.i_done,name='i_done'),
    path('p_done',views.p_done,name='p_done'),
    path('logout',views.logout.as_view(),name='logout')
]


