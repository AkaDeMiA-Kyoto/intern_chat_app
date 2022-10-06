from xml.dom.minidom import Document
from django.conf import settings
from django.urls import path, include
from . import views
from .views import PasswordChange, Logout#, Login, Signup 
from django.conf.urls.static import static

import debug_toolbar

urlpatterns = [
    path('', views.index, name='index'),
    #path('signup', Signup.as_view(), name='signup_view'),
    #path('login', Login.as_view(), name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:pk>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path("pass_change", PasswordChange.as_view(), name="pass_change"),
    path("pass_change_done", views.pass_change_done, name="pass_change_done"),    
    path("name_change", views.name_change, name="name_change"),
    path("name_change_done", views.name_change_done, name="name_change_done"),        
    path("mail_change", views.mail_change, name="mail_change"),
    path("mail_change_done", views.mail_change_done, name="mail_change_done"),        
    path("icon_change", views.icon_change, name="icon_change"),
    path("icon_change_done", views.icon_change_done, name="icon_change_done"),    
    path("logout", Logout.as_view(), name="logout"),    
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)