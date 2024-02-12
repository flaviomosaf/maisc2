from django.urls import path
from django.contrib import admin
from room import views

app_name = 'room'

urlpatterns = [
    path('', views.rooms_home, name='rooms_home'),
    path('<slug:slug>/', views.room_chat, name='room_chat'),
]