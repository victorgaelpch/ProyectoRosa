from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Sucursal, Pedido, PedidoPickup, DetallePedido
from .forms import PedidoPickupForm
from menu.models import Producto
import json
from django.utils import timezone


def seleccionar_tipo_pedido(request):
    return render(request, 'pedido/tipo_pedido.html')


@login_required
def pickup_pedido(request):
    sucursales = Sucursal.objects.all()
    productos = Producto.objects.all()

    if request.method == 'POST':
        form = PedidoPickupForm(request.POST)
        sucursal_id = request.POST.get('sucursal')
        carrito_json = request.POST.get('carrito_json')
        tipo_pago = request.POST.get('tipo_pago')
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')

        # Validaciones básicas
        if not sucursal_id:
            messages.error(request, "Debes seleccionar una sucursal.")
        elif not carrito_json or carrito_json == "[]":
            messages.error(request, "El carrito no puede estar vacío.")
        elif not tipo_pago:
            messages.error(request, "Debes seleccionar un método de pago.")
        elif tipo_pago == "efectivo" and (not nombre or not correo or not telefono):
            messages.error(
                request, "Debes completar tus datos para pago en efectivo.")
        elif not form.is_valid():
            messages.error(request, "Debes seleccionar un horario válido.")
        else:
            try:
                horario = form.cleaned_data['horario_recoleccion']
                sucursal = Sucursal.objects.get(id=sucursal_id)
                carrito = json.loads(carrito_json)

                # Crear el pedido principal
                pedido = Pedido.objects.create(
                    usuario=request.user,
                    sucursal=sucursal,
                    estado='pendiente',
                    fecha_hora=timezone.now(),
                    total=0  # Se actualiza después
                )

                # Crear el pedido pickup
                PedidoPickup.objects.create(
                    pedido=pedido,
                    horario_recoleccion=horario,
                    tipo_pago=tipo_pago
                )

                # Guardar los detalles del pedido y calcular el total
                total = 0
                for item in carrito:
                    producto = Producto.objects.get(id=item['id'])
                    cantidad = int(item['cantidad'])
                    subtotal = producto.precio * cantidad
                    DetallePedido.objects.create(
                        pedido=pedido,
                        producto=producto,
                        cantidad=cantidad,
                        subtotal=subtotal
                    )
                    total += subtotal

                # Actualizar el total del pedido
                pedido.total = total
                pedido.save()

                # Aquí podrías guardar los datos de contacto si es efectivo (opcional)
                # ...

                return render(request, 'pedido/pickup_exito.html', {
                    'sucursal': sucursal,
                    'horario': horario,
                    'pedido': pedido,
                })
            except Exception as e:
                messages.error(
                    request, f"Ocurrió un error al procesar el pedido: {str(e)}")

    else:
        form = PedidoPickupForm()

    return render(request, 'pedido/pickup.html', {
        'sucursales': sucursales,
        'form': form,
        'productos': productos,
    })


@login_required
def detalle_pedido_pickup(request, pedido_id):
    pedido = Pedido.objects.select_related('sucursal', 'pickup').prefetch_related(
        'detallespedido_set__producto').get(id=pedido_id)
    return render(request, 'pedido/detalle_pedido_pickup.html', {'pedido': pedido})


@login_required
def lista_pedidos_pickup(request):

    pedidos = Pedido.objects.filter(
        pickup__isnull=False,
        estado__in=['pendiente', 'preparando']
    ).select_related('sucursal', 'pickup').order_by('pickup__horario_recoleccion')

    return render(request, 'pedido/lista_pedidos_pickup.html', {
        'pedidos': pedidos,
    })


def kiosko_pedido(request):
    return render(request, 'pedido/kiosko.html')
