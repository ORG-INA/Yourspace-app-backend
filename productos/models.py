from django.db import models
from cloudinary.models import CloudinaryField

    
class Marca(models.Model):
    id_marca = models.AutoField(primary_key=True)
    nombre_marca = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nombre_marca

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=45)
    id_categoria_padre = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nombre_categoria
    
class TemporadaEvento(models.Model):
    id_temporada_evento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, null=True)
    fecha_inicio = models.DateField(null=True)
    fecha_fin = models.DateField(null=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    imagen = CloudinaryField('image', null=True, blank=True)
    marca = models.ForeignKey(Marca, null=True, blank=True, on_delete=models.SET_NULL)
    categorias = models.ManyToManyField(Categoria)
    temporadas_evento = models.ManyToManyField(TemporadaEvento, related_name='productos', blank=True)
    update_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.nombre
    
