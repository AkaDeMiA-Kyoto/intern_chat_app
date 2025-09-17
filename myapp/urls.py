from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup_view'),
    path('login/', views.login_view.as_view(), name='login_view'),
    path('friends/', views.friends, name='friends'),
    path('talk_room/<int:friend_id>/', views.talk_room, name='talk_room'),
    path('setting/', views.setting, name='setting'),
    path('setting_username/', views.setting_username, name='setting_username'),
    path('setting_email/', views.setting_email, name='setting_email'),
    path('setting_icon/', views.setting_icon, name='setting_icon'),
    path('setting_password/', views.setting_password, name='setting_password'),
    path('setting_logout/', views.setting_logout.as_view(), name='setting_logout'),
    path('setting_complete/', views.setting_complete, name='setting_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
