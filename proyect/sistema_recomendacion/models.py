from django.db import models
from menu.models import Producto


class ProductoRelacionado(models.Model):
    producto_principal = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name='productos_relacionados')
    producto_relacionado = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name='productos_que_lo_relacionan')
    # Un valor que represente la "fuerza" de la relación (ej. soporte, confianza, frecuencia)
    score = models.FloatField(default=0.0)
    # Fecha de la última actualización del cálculo
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('producto_principal', 'producto_relacionado')
        # Evita duplicados y mejora rendimiento en búsquedas
        indexes = [
            models.Index(fields=['producto_principal']),
            models.Index(fields=['producto_relacionado']),
        ]

    def __str__(self):
        return f"{self.producto_principal.nombre_producto} -> {self.producto_relacionado.nombre_producto} (Score: {self.score})"
