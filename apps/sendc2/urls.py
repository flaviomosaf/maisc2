from django.urls import path 
from django.contrib.auth import views as auth_views 
from sendc2 import views

app_name = 'sendc2' 

urlpatterns = [
    path('', views.sendc2_home, name='sendc2_home'),
    path('send/', views.sendc2_message, name='sendc2_message'),
]

