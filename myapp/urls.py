from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'myapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup_view'),
    path('login/', views.login_view, name='login_view'),
    path('friends/', views.friends, name='friends'),
    path('talk_room/<int:user_id>/', views.talk_room, name='talk_room'),
    path('setting/', views.setting, name='setting'),
    path('logout/', views.logout_view, name='logout_view'),
    path('username_update/', views.username_update, name='username_update'),
    path('email_update/', views.email_update, name='email_update'),
    path('password_update/', views.password_update, name='password_update'),
    path('img_update/', views.img_update, name='img_update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)