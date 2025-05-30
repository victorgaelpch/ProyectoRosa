from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from pedido.models import Pedido
from pedido.views import sumar_puntos_a_cliente  # Importa tu función de puntos


@staff_member_required
def caja_buscar_pedido(request):
    pedido = None
    mensaje = None
    productos_puntos = []
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '').upper()
        nuevo_estado = request.POST.get('nuevo_estado')
        try:
            pedido = Pedido.objects.select_related('pickup').get(codigo=codigo)
            if nuevo_estado and nuevo_estado in ['pagado', 'recogido']:
                # Solo suma puntos si el pedido no estaba ya pagado
                if pedido.estado != 'pagado' and nuevo_estado == 'pagado':
                    puntos_ganados = sumar_puntos_a_cliente(
                        pedido.usuario, pedido)
                    pedido.puntos_ganados = puntos_ganados
                pedido.estado = nuevo_estado
                pedido.save()
                mensaje = f"Estado actualizado a {nuevo_estado}."
        except Pedido.DoesNotExist:
            mensaje = "No se encontró un pedido con ese código."
    elif request.method == 'GET':
        codigo = request.GET.get('codigo', '').upper()
        if codigo:
            try:
                pedido = Pedido.objects.select_related(
                    'pickup').get(codigo=codigo)
                if pedido:
                    for detalle in pedido.detalles.all():
                        puntos = detalle.producto.puntos_extra * detalle.cantidad
                        productos_puntos.append({
                            'nombre': detalle.producto.nombre_producto,
                            'cantidad': detalle.cantidad,
                            'subtotal': detalle.subtotal,
                            'puntos_extra': puntos,
                        })
            except Pedido.DoesNotExist:
                mensaje = "No se encontró un pedido con ese código."

    return render(request, 'caja/caja_buscar_pedido.html', {
        'pedido': pedido,
        'mensaje': mensaje,
        'productos_puntos': productos_puntos,
    })


@staff_member_required
def eliminar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.delete()
    return redirect('caja_buscar_pedido')
