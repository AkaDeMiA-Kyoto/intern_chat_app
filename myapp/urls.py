from django.urls import path
from . import views
from intern import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('login', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('friends', views.friends, name='friends'),
    path('talk_room', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('talk_room/<int:user_id>/', views.talk_room, name='talk_room' )
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
