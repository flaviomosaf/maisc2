from rest_framework import serializers
from .models import Analytic
from django.shortcuts import render

class AnalyticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analytic
        fields = ['id', 'message_raw',]