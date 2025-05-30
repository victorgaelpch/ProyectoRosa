from django.db import models

# Create your models here.


class Producto(models.Model):
    nombre_producto = models.CharField(
        max_length=100
    )  # Nombre del producto (ej: "Café Americano", "Croissant")
    tamaño = models.CharField(
        max_length=20
    )  # Tamaño del producto (ej: "Chico", "Grande", "Individual")
    descripcion = models.TextField()  # Descripción del producto
    imagen = models.ImageField(
        upload_to='media/productos/'
    )  # Imagen del producto
    precio = models.DecimalField(
        max_digits=8, decimal_places=2
    )  # Precio del producto
    tipo = models.CharField(
        max_length=30
    )  # Tipo general (ej: "bebida caliente", "bocadillo", etc.)
    puntos_extra = models.PositiveIntegerField(
        default=0, help_text="Puntos extra por comprar este producto")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return (
            f' NombreProducto={self.nombre_producto}, Tamaño={self.tamaño}, '
            f'Descripcion={self.descripcion}, Imagen={self.imagen}, '
            f'Precio={self.precio}, Tipo={self.tipo}'
        )

# Subclase para bebidas calientes


class BebidaCaliente(Producto):
    tipo_vaso = models.CharField(
        max_length=20
    )  # Tipo de vaso (ej: "Carton", "Ceramica")
    tipo_leche = models.CharField(
        max_length=30
    )  # Tipo de leche (ej: "Entera", "Almendra")
    sabor = models.CharField(
        max_length=30
    )  # Sabor de la bebida (ej: "Vainilla", "Chocolate")

# Subclase para bebidas frías


class BebidaFria(Producto):
    tipo_vaso = models.CharField(
        max_length=20
    )  # Tipo de vaso (ej: "Plástico", "Vidrio")
    tipo_hielo = models.CharField(
        max_length=30
    )  # Tipo de hielo (ej: "Normal", "Triturado")
    sabor = models.CharField(
        max_length=30
    )  # Sabor de la bebida fría

# Subclase para bocadillos (sandwiches, etc.)


class Bocadillo(Producto):
    tipo_pan = models.CharField(
        max_length=30
    )  # Tipo de pan (ej: "Baguette", "Integral")
    relleno = models.TextField()  # Descripción del relleno

# Subclase para snacks (botanas)


class Snack(Producto):
    tipo_snack = models.CharField(
        max_length=30
    )  # Tipo de snack (ej: "Papas", "Nachos")
    tipo_sabor = models.CharField(
        max_length=30
    )  # Sabor del snack (ej: "Queso", "Chile")

# Subclase para repostería (pasteles, galletas, etc.)


class Reposteria(Producto):
    tipo_reposteria = models.CharField(
        max_length=30
    )  # Tipo de repostería (ej: "Pastel", "Brownie")
    glaseado = models.BooleanField(
        default=False
    )  # ¿Tiene glaseado?
    decorado = models.BooleanField(
        default=False
    )  # ¿Está decorado?
    sabor = models.CharField(
        max_length=30
    )  # Sabor principal (ej: "Chocolate", "Vainilla")
