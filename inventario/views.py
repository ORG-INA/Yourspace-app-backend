from rest_framework import viewsets
from .models import Inventario, AdquisicionInventario
from .serializers import InventarioSerializer, AdquisicionInventarioSerializer

class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer

class AdquisicionInventarioViewSet(viewsets.ModelViewSet):
    queryset = AdquisicionInventario.objects.all()
    serializer_class = AdquisicionInventarioSerializer
