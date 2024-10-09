from django.urls import path, include
from . import views

appname = 'myapp'

urlpatterns = [
    path('account_signup/', views.SignUp.as_view(), name='signup'),
]
