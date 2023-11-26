import datetime
from rest_framework import serializers
from .models import Categoria, Marca, Producto, TemporadaEvento

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'
    
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'
        
class TemporadaEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporadaEvento
        fields = '__all__'
        
class ProductoSerializer(serializers.ModelSerializer):
    # categorias = CategoriaSerializer(many=True, read_only=True)
    # temporadas_evento = TemporadaEventoSerializer(many=True, read_only=True)
    # marca = MarcaSerializer(read_only=True)

    class Meta:
        model = Producto
        fields = '__all__'
        

class IngresarProductoEInventarioSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=255)
    descripcion = serializers.CharField(allow_null=True, required=False)
    precio = serializers.DecimalField(max_digits=10, decimal_places=2)
    descuento = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True, required=False)
    imagen = serializers.ImageField(required=False) 
    marca = serializers.PrimaryKeyRelatedField(queryset=Marca.objects.all(), allow_null=True, required=False)
    categorias = serializers.PrimaryKeyRelatedField(many=True, queryset=Categoria.objects.all(), required=False)
    temporadas_evento = serializers.PrimaryKeyRelatedField(many=True, queryset=TemporadaEvento.objects.all(), required=False)
    cantidad = serializers.IntegerField()
    fecha = serializers.DateTimeField(required=False, default=datetime.datetime.now())
    
    def update(self, instance, validated_data):
        # print("update", instance, validated_data)
        
        # Actualiza los campos del objeto instance con los datos validados
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.precio = validated_data.get('precio', instance.precio)
        instance.descuento = validated_data.get('descuento', instance.descuento)
        instance.marca = validated_data.get('marca', instance.marca)
        instance.imagen = validated_data.get('imagen', instance.imagen)
        # Actualiza las relaciones 'categorias' y 'temporadas_evento' si es necesario
        instance.categorias.set(validated_data.get('categorias', instance.categorias.all()))
        instance.temporadas_evento.set(validated_data.get('temporadas_evento', instance.temporadas_evento.all()))
        instance.save()  # Guarda los cambios en la base de datos
        
        return instance
