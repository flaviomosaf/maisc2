from rest_framework import viewsets
from .serializers import AnalyticSerializer
from .models import Analytic

class AnalyticViewSet(viewsets.ModelViewSet):
    serializer_class = AnalyticSerializer
    queryset = Analytic.objects.all()

    
