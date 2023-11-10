from rest_framework import viewsets

from main.permissions import IsStaffUser
from .models import Inventario, AdquisicionInventario
from .serializers import InventarioSerializer, AdquisicionInventarioSerializer

class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsStaffUser()]
        return []

class AdquisicionInventarioViewSet(viewsets.ModelViewSet):
    queryset = AdquisicionInventario.objects.all()
    serializer_class = AdquisicionInventarioSerializer
    permission_classes = [IsStaffUser]
