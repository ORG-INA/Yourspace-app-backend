from rest_framework import serializers
from .models import Inventario, AdquisicionInventario

class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        fields = '__all__'

class AdquisicionInventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdquisicionInventario
        fields = '__all__'
