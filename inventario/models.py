from django.db import models
from compras.models import Compra

from productos.models import Producto

# Create your models here.
class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)
    cantidad_disponible = models.IntegerField(null=True)

    def __str__(self):
        return f"Inventario de {self.producto.nombre}"
    
class AdquisicionInventario(models.Model):
    id_adquisicion_inventario = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    cantidad = models.IntegerField(null=True)
    fecha = models.DateTimeField(auto_now=True, null=True)
    precio_unidad = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"Adquisición de {self.producto.producto.nombre}"
    
# class TransaccionVentaInventario(models.Model):
#     id_transaccion_venta = models.AutoField(primary_key=True)
#     producto = models.ForeignKey(Inventario, on_delete=models.CASCADE)
#     compra = models.ForeignKey(Compra, null=True, on_delete=models.SET_NULL)
#     cantidad = models.IntegerField(null=True)
#     fecha = models.DateTimeField(null=True)

#     def __str__(self):
#         return f"Transacción de venta de {self.producto.producto.nombre}"