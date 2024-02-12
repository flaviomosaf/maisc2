from django.contrib import admin
from django.urls import path, include
from analytic import views
from rest_framework import routers
from .views import AnalyticViewSet

router = routers.DefaultRouter()
router.register('analytic', AnalyticViewSet)

urlpatterns = [
    path('', include(router.urls)),
]