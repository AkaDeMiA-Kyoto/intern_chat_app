from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "myapp"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signup/', views.UserSignupView.as_view(), name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('friends/', views.friends, name='friends'),
    path('talk_room/', views.talk_room, name='talk_room'),
    path('setting/', views.setting, name='setting'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
