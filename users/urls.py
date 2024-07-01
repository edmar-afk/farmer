from django.urls import path
from . import views

urlpatterns = [
    
    path('mainLogin', views.mainLogin, name='mainLogin'),
    path('mainDashboard', views.mainDashboard, name='mainDashboard'),
    path('logInInfo', views.logInInfo, name='logInInfo'),
    path('<int:user_id>/removeUser/', views.removeUser, name='removeUser'),
    path('acceptUser/<int:user_id>/', views.acceptUser, name='acceptUser'),
    path('declineUser/<int:user_id>/', views.declineUser, name='declineUser'),
    
    
    path('login', views.login, name='login'),
    path('homepage', views.homepage, name='homepage'),
    path('register', views.register, name='register'),

    
    path('farmerDashboard', views.farmerDashboard, name='farmerDashboard'),
    
    path('logoutUser', views.logoutUser, name='logoutUser'),
]