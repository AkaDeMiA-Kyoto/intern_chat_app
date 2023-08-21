from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import friends



urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.SignUpView.as_view(), name='signup_view'),
    path('login', views.loginview.as_view(), name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:user_id>/', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
