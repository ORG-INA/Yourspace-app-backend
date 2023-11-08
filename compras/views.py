from rest_framework import viewsets
from .models import Carro, CarroProductos, Compra
from .serializers import CarroSerializer, CarroProductosSerializer, CompraSerializer

class CarroViewSet(viewsets.ModelViewSet):
    queryset = Carro.objects.all()
    serializer_class = CarroSerializer

class CarroProductosViewSet(viewsets.ModelViewSet):
    queryset = CarroProductos.objects.all()
    serializer_class = CarroProductosSerializer

class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer
    