from django.db import models

from productos.models import Producto
from usuarios.models import User


# Create your models here.
class Carro(models.Model):
    id_carro = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Compra {self.idCompra} realizada por {self.idUsuario}"
    
class CarroProductos(models.Model):
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"Compra de {self.cantidad} {self.producto.nombre} por {self.precio} cada uno"

class Compra(models.Model):
    id_compra = models.AutoField(primary_key=True)
    carro = models.OneToOneField(Carro, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Compra {self.idCompra} asociada al carro {self.carro.idCarro}"