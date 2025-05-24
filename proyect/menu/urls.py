from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('productos/<int:producto_id>/editar/',
         views.editar_producto, name='editar_producto'),
    path('productos/<int:producto_id>/eliminar/',
         views.eliminar_producto, name='eliminar_producto'),
]
