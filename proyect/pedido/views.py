from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Sucursal, Pedido, PedidoPickup, DetallePedido
from .forms import PedidoPickupForm
from menu.models import Producto
import json
from django.utils import timezone
from decimal import Decimal


def seleccionar_tipo_pedido(request):
    return render(request, 'pedido/tipo_pedido.html')


@login_required
def pickup_pedido(request):
    # Obtén datos del usuario
    nombre = request.user.get_full_name() or ''
    correo = request.user.email or ''
    telefono = ''
    perfil = request.user.perfil if hasattr(request.user, 'perfil') else None
    if perfil:
        telefono = perfil.telefono or ''

    sucursales = Sucursal.objects.all()
    productos = Producto.objects.all()
    form = PedidoPickupForm()

    VALOR_PUNTO = Decimal('0.50')  # ahora es Decimal

    if request.method == 'POST':
        form = PedidoPickupForm(request.POST)
        tipo_pago = request.POST.get('tipo_pago')
        nombre_post = request.POST.get('nombre')
        correo_post = request.POST.get('correo')
        telefono_post = request.POST.get('telefono')
        carrito_json = request.POST.get('carrito_json')
        carrito = json.loads(carrito_json) if carrito_json else []

        # Validación básica para efectivo
        if tipo_pago == 'efectivo':
            if not nombre_post or not correo_post or not telefono_post:
                messages.error(
                    request, "Debes completar todos los datos para pago en efectivo.")
                return render(request, 'pedido/pickup.html', {
                    'sucursales': sucursales,
                    'form': form,
                    'productos': productos,
                    'nombre': nombre_post,
                    'correo': correo_post,
                    'telefono': telefono_post,
                })

        if form.is_valid():
            horario_recoleccion = form.cleaned_data['horario_recoleccion']
            sucursal_id = request.POST.get('sucursal')
            sucursal = Sucursal.objects.get(id=sucursal_id)

            # Calcular total del carrito
            total = 0
            for item in carrito:
                producto = Producto.objects.get(id=item['id'])
                cantidad = int(item['cantidad'])
                subtotal = producto.precio * cantidad
                total += subtotal

            # Pago con puntos
            puntos_a_usar = int(request.POST.get('puntos_a_usar', 0))
            max_puntos = min(perfil.puntos if perfil else 0,
                             int(total // VALOR_PUNTO))
            puntos_a_usar = min(puntos_a_usar, max_puntos)
            total_final = total - (puntos_a_usar * VALOR_PUNTO)

            # Si el total final es 0, el pedido se marca como pagado
            estado_pedido = 'pagado' if total_final == 0 else 'pendiente'

            # Crea el pedido con el total final y puntos usados
            pedido = Pedido.objects.create(
                usuario=request.user,
                sucursal=sucursal,
                estado=estado_pedido,
                total=total_final,
                puntos_usados=puntos_a_usar,
            )

            # Crea los detalles del pedido
            for item in carrito:
                producto = Producto.objects.get(id=item['id'])
                cantidad = int(item['cantidad'])
                subtotal = producto.precio * cantidad
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=cantidad,
                    subtotal=subtotal,
                )

            # Descuenta los puntos del perfil
            if perfil and puntos_a_usar > 0:
                perfil.puntos -= puntos_a_usar
                perfil.save()

            # Crea el objeto Pickup relacionado
            PedidoPickup.objects.create(
                pedido=pedido,
                horario_recoleccion=horario_recoleccion,
                tipo_pago=tipo_pago,
            )

            # Guardar datos en el perfil si no existen
            user = request.user
            if tipo_pago == 'efectivo':
                if not user.first_name and nombre_post:
                    user.first_name = nombre_post.split()[0]
                    if len(nombre_post.split()) > 1:
                        user.last_name = " ".join(nombre_post.split()[1:])
                if not user.email and correo_post:
                    user.email = correo_post
                user.save()
                if perfil and not perfil.telefono and telefono_post:
                    perfil.telefono = telefono_post
                    perfil.save()
            # Redirige a la pantalla de éxito
            return redirect('pickup_exito_estado', pedido_id=pedido.id)
    tipos = Producto.objects.values_list('tipo', flat=True).distinct()
    return render(request, 'pedido/pickup.html', {
        'sucursales': sucursales,
        'form': form,
        'productos': productos,
        'tipos': tipos,
        'nombre': nombre,
        'correo': correo,
        'telefono': telefono,
        'perfil': perfil,  # Para mostrar puntos disponibles en el template
    })


@login_required
def pickup_exito_estado(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    return render(request, 'pedido/pickup_exito.html', {
        'pedido': pedido,
        'sucursal': pedido.sucursal,
        'horario': pedido.pickup.horario_recoleccion,
    })


@login_required
def cancelar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    if pedido.estado == 'pendiente':
        pedido.estado = 'cancelado'
        pedido.save()
    return redirect('lista_pedidos_pickup')


@login_required
def detalle_pedido_pickup(request, pedido_id):
    pedido = Pedido.objects.select_related('sucursal', 'pickup').prefetch_related(
        'detallespedido_set__producto').get(id=pedido_id)
    return render(request, 'pedido/detalle_pedido_pickup.html', {'pedido': pedido})


@login_required
def lista_pedidos_pickup(request):
    mostrar_recogidos = request.GET.get('mostrar_recogidos') == '1'
    mostrar_cancelados = request.GET.get('mostrar_cancelados') == '1'

    estados = ['pendiente', 'preparando', 'pagado']
    if mostrar_recogidos:
        estados.append('recogido')
    if mostrar_cancelados:
        estados.append('cancelado')
    pedidos = Pedido.objects.filter(
        pickup__isnull=False,
        estado__in=estados,
        usuario=request.user  # Si solo quieres mostrar los pedidos del usuario actual
    ).select_related('sucursal', 'pickup').order_by('pickup__horario_recoleccion')

    return render(request, 'pedido/lista_pedidos_pickup.html', {
        'pedidos': pedidos,
        'mostrar_recogidos': mostrar_recogidos,
        'mostrar_cancelados': mostrar_cancelados,
    })


def sumar_puntos_a_cliente(usuario, pedido):
    if not usuario or not hasattr(usuario, 'perfil'):
        return 0  # No sumar puntos si no hay usuario o perfil
    perfil = usuario.perfil
    puntos_por_total = int(pedido.total // 30) * 5
    puntos_extra = sum([detalle.producto.puntos_extra *
                       detalle.cantidad for detalle in pedido.detalles.all()])
    total_puntos = puntos_por_total + puntos_extra
    perfil.puntos += total_puntos
    perfil.save()
    return total_puntos


def usar_puntos_en_pedido(usuario, pedido):
    perfil = usuario.perfil
    # Por ejemplo: 1 punto = $1 de descuento
    puntos_a_usar = min(perfil.puntos, int(pedido.total))
    pedido.total -= puntos_a_usar
    perfil.puntos -= puntos_a_usar
    perfil.save()
    pedido.save()
    return puntos_a_usar


@login_required
def puntos_recompensas(request):
    perfil = request.user.perfil
    pedidos = Pedido.objects.filter(
        usuario=request.user, estado='pagado'
    ).order_by('-fecha_hora')
    pedidos_con_detalles = []
    for pedido in pedidos:
        detalles = []
        for detalle in pedido.detalles.all():
            detalles.append({
                'nombre': detalle.producto.nombre_producto,
                'cantidad': detalle.cantidad,
                'puntos_extra': detalle.producto.puntos_extra * detalle.cantidad,
            })
        pedidos_con_detalles.append({
            'pedido': pedido,
            'detalles': detalles,
        })
    return render(request, 'pedido/puntos_recompensas.html', {
        'perfil': perfil,
        'pedidos_con_detalles': pedidos_con_detalles,
    })


@csrf_exempt
def kiosko_pedido(request):
    productos = Producto.objects.all()
    sucursales = Sucursal.objects.all()
    tipos = Producto.objects.values_list('tipo', flat=True).distinct()
    mensaje = None
    VALOR_PUNTO = Decimal('0.50')

    if request.method == 'POST':
        sucursal_id = request.POST.get('sucursal')
        sucursal = Sucursal.objects.get(id=sucursal_id)
        carrito_json = request.POST.get('carrito_json')
        carrito = json.loads(carrito_json) if carrito_json else []
        nombre = request.POST.get('nombre', '').strip()
        telefono = request.POST.get('telefono', '').strip()

        # Calcular total
        total = Decimal('0')
        for item in carrito:
            producto = Producto.objects.get(id=item['id'])
            cantidad = int(item['cantidad'])
            subtotal = producto.precio * cantidad
            total += subtotal

        # Si el usuario está autenticado, aplica lógica de puntos igual que pickup
        if request.user.is_authenticated and hasattr(request.user, 'perfil'):
            perfil = request.user.perfil
            puntos_a_usar = int(request.POST.get('puntos_a_usar', 0))
            max_puntos = min(perfil.puntos, int(total // VALOR_PUNTO))
            puntos_a_usar = min(puntos_a_usar, max_puntos)
            total_final = total - (puntos_a_usar * VALOR_PUNTO)
            estado_pedido = 'pagado' if total_final == 0 else 'pendiente'
            pedido = Pedido.objects.create(
                usuario=request.user,
                sucursal=sucursal,
                estado=estado_pedido,
                total=total_final,
                puntos_usados=puntos_a_usar,
            )
            # Descuenta los puntos del perfil
            if puntos_a_usar > 0:
                perfil.puntos -= puntos_a_usar
                perfil.save()
        else:
            # Pedido anónimo, sin puntos
            pedido = Pedido.objects.create(
                usuario=None,
                sucursal=sucursal,
                estado='pendiente',
                total=total,
                puntos_ganados=0,
                puntos_usados=0,
            )

        # Crea los detalles del pedido
        for item in carrito:
            producto = Producto.objects.get(id=item['id'])
            cantidad = int(item['cantidad'])
            subtotal = producto.precio * cantidad
            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad,
                subtotal=subtotal,
            )

        # Crea el objeto Pickup relacionado (puedes poner horario actual)
        PedidoPickup.objects.create(
            pedido=pedido,
            horario_recoleccion=timezone.now(),
            tipo_pago='kiosko',
        )

        # Si el usuario está autenticado, suma puntos ganados
        if request.user.is_authenticated and hasattr(request.user, 'perfil') and pedido.total > 0:
            puntos_por_total = int(pedido.total // 30) * 5
            puntos_extra = sum([
                detalle.producto.puntos_extra * detalle.cantidad
                for detalle in pedido.detalles.all()
            ])
            total_puntos = puntos_por_total + puntos_extra
            perfil = request.user.perfil
            perfil.puntos += total_puntos
            perfil.save()
            pedido.puntos_ganados = total_puntos
            pedido.save()

        mensaje = f"¡Pedido realizado! Código: {pedido.codigo}"

        return render(request, 'pedido/kiosko_exito.html', {
            'pedido': pedido,
            'mensaje': mensaje,
            'nombre': nombre,
            'telefono': telefono,
        })

    return render(request, 'pedido/kiosko.html', {
        'productos': productos,
        'sucursales': sucursales,
        'tipos': tipos,
    })
