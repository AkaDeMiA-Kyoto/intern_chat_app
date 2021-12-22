from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import static, urlpatterns
urlpatterns=[
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view, name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:num>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('setting_name', views.setting_name, name='setting_name'),
    path('setting_mail', views.setting_mail, name='setting_mail'),
    path('setting_img', views.setting_img, name='setting_img'),
    path('setting_password', views.setting_password, name='setting_password'),
   
] 

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)