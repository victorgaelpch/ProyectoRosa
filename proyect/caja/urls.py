from django.urls import path
from . import views

urlpatterns = [
    path('caja/', views.caja_buscar_pedido, name='caja_buscar_pedido'),
    path('eliminar/<int:pedido_id>/',
         views.eliminar_pedido, name='eliminar_pedido'),
]
