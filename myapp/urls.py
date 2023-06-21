from django.urls import path,include
from . import views
# from .views import index_view
from django.conf import settings
from django.conf.urls.static import static
from .views import friendslist
from .views import TalkRoom,Logout
from .models import CustomUser

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup_view'),
    path('login/', views.CustomLoginView.as_view() , name='login_view'),
    path('friends/', views.friendslist.as_view(), name='friends'),
    path('setting/', views.Setting.as_view(), name='setting'),
    path('talk_room/<int:pk>',TalkRoom.as_view(),name ='talk_room'),   
    path('logout/',Logout.as_view(),name="logout") ,
    path('user/<int:pk>',views.UserView.as_view(),name='user_view'),
    path('email/<int:pk>',views.EmailView.as_view(),name='email_view'),
    path('icon/<int:pk>',views.IconView.as_view(),name='icon_view'),
    path('password/<int:pk>',views.PasswordChange.as_view(),name='password_change'),
    path('finish/',views.finish_view,name='finish_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)