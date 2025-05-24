from django.db import models

# Create your models here.


class Producto(models.Model):
    nombre_producto = models.CharField(max_length=100)
    tamaño = models.CharField(max_length=20)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='media/productos/')
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    tipo = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f' NombreProducto={self.nombre_producto}, Tamaño={self.tamaño}, Descripcion={self.descripcion}, Imagen={self.imagen}, Precio={self.precio}, Tipo={self.tipo}'


class BebidaCaliente(Producto):
    tipo_vaso = models.CharField(max_length=20)
    tipo_leche = models.CharField(max_length=30)
    sabor = models.CharField(max_length=30)


class BebidaFria(Producto):
    tipo_vaso = models.CharField(max_length=20)
    tipo_hielo = models.CharField(max_length=30)
    sabor = models.CharField(max_length=30)


class Bocadillo(Producto):
    tipo_pan = models.CharField(max_length=30)
    relleno = models.TextField()


class Snack(Producto):
    tipo_snack = models.CharField(max_length=30)
    tipo_sabor = models.CharField(max_length=30)


class Reposteria(Producto):
    tipo_reposteria = models.CharField(max_length=30)
    glaseado = models.BooleanField(default=False)
    decorado = models.BooleanField(default=False)
    sabor = models.CharField(max_length=30)
