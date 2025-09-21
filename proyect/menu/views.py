from .models import Producto
from django.contrib.auth.decorators import user_passes_test
from .forms import ProductoForm, BebidaCalienteForm, BebidaFriaForm, BocadilloForm, SnackForm, ReposteriaForm
from django.shortcuts import render, redirect, get_object_or_404


def lista_productos(request):
    tipo = request.GET.get('tipo')
    productos = Producto.objects.all()
    tipos = Producto.objects.values_list('tipo', flat=True).distinct()
    if tipo:
        productos = productos.filter(tipo=tipo)
    es_gerente = request.user.is_authenticated and request.user.groups.filter(
        name='Gerente').exists()
    return render(request, 'menu/lista_productos.html', {
        'productos': productos,
        'tipos': tipos,
        'tipo_seleccionado': tipo,
        'es_gerente': es_gerente,
    })


def es_gerente(user):
    return user.is_authenticated and user.groups.filter(name='Gerente').exists()


@user_passes_test(es_gerente)
def agregar_producto(request):
    es_gerente_flag = es_gerente(request.user)
    tipo = request.GET.get('tipo') or request.POST.get('tipo')
    form = None

    if tipo == 'bebida_caliente':
        FormClass = BebidaCalienteForm
    elif tipo == 'bebida_fria':
        FormClass = BebidaFriaForm
    elif tipo == 'bocadillo':
        FormClass = BocadilloForm
    elif tipo == 'snack':
        FormClass = SnackForm
    elif tipo == 'reposteria':
        FormClass = ReposteriaForm
    else:
        FormClass = ProductoForm

    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = FormClass()

    return render(request, 'menu/agregar_producto.html', {
        'form': form,
        'es_gerente': es_gerente_flag,
        'tipo': tipo
    })


@user_passes_test(es_gerente)
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    es_gerente_flag = es_gerente(request.user)

    if hasattr(producto, 'bebidacaliente'):
        instancia = producto.bebidacaliente
        FormClass = BebidaCalienteForm
        tipo = 'bebida_caliente'
    elif hasattr(producto, 'bebidafria'):
        instancia = producto.bebidafria
        FormClass = BebidaFriaForm
        tipo = 'bebida_fria'
    elif hasattr(producto, 'bocadillo'):
        instancia = producto.bocadillo
        FormClass = BocadilloForm
        tipo = 'bocadillo'
    elif hasattr(producto, 'snack'):
        instancia = producto.snack
        FormClass = SnackForm
        tipo = 'snack'
    elif hasattr(producto, 'reposteria'):
        instancia = producto.reposteria
        FormClass = ReposteriaForm
        tipo = 'reposteria'
    else:
        instancia = producto
        FormClass = ProductoForm
        tipo = producto.tipo

    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES, instance=instancia)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = FormClass(instance=instancia)

    return render(request, 'menu/editar_producto.html', {
        'form': form,
        'producto': producto,
        'es_gerente': es_gerente_flag,
        'tipo': tipo
    })


@user_passes_test(es_gerente)
def eliminar_producto(request, producto_id):
    try:
        producto = Producto.objects.get(id=producto_id)
        producto.delete()
    except Producto.DoesNotExist:
        pass
    return redirect('lista_productos')
