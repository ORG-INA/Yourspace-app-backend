from rest_framework import serializers
from .models import Carro, CarroProductos, Compra

class CarroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carro
        fields = '__all__'

class CarroProductosSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarroProductos
        fields = '__all__'

class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = '__all__'
