from django.urls import path
from . import views

urlpatterns = [
    path('pesticides', views.pesticides, name='pesticides'),
    path('mainLogin', views.mainLogin, name='mainLogin'),
    path('mainDashboard', views.mainDashboard, name='mainDashboard'),
    path('logInInfo', views.logInInfo, name='logInInfo'),
    
    path('<int:product_id>/removeProduct/', views.removeProduct, name='removeProduct'),
    path('<int:user_id>/removeUser/', views.removeUser, name='removeUser'),
    path('acceptUser/<int:user_id>/', views.acceptUser, name='acceptUser'),
    path('declineUser/<int:user_id>/', views.declineUser, name='declineUser'),
    
    
    path('login', views.login, name='login'),
    path('homepage', views.homepage, name='homepage'),
    path('register', views.register, name='register'),

    path('pest', views.pest, name='pest'),
    path('cropSeason', views.cropSeason, name='cropSeason'),
    path('farmerFertilizer', views.farmerFertilizer, name='farmerFertilizer'),
    path('farmerDashboard', views.farmerDashboard, name='farmerDashboard'),
    
    path('logoutUser', views.logoutUser, name='logoutUser'),
]