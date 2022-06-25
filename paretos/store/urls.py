from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout_user'),
    path('logout_view', views.logout_view, name='logout_view'),
    path('register', views.register_user, name='register_user'),
    path('test', views.test, name='test'),
    path('confirmation', views.email_activation, name='confirmation'),
    path('request_reset_password',
         views.request_reset_password,
         name='request_reset_password'),
    path('reset/<str:username>/', views.reset_password, name='reset_password'),
]
