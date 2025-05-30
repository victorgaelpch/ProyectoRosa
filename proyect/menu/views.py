from .models import Producto
from django.contrib.auth.decorators import user_passes_test
from .forms import ProductoForm
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
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'menu/agregar_producto.html', {'form': form, 'es_gerente': es_gerente_flag})


@user_passes_test(es_gerente)
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    es_gerente_flag = es_gerente(request.user)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'menu/editar_producto.html', {'form': form, 'producto': producto, 'es_gerente': es_gerente_flag})


@user_passes_test(es_gerente)
def eliminar_producto(request, producto_id):
    try:
        producto = Producto.objects.get(id=producto_id)
        producto.delete()
    except Producto.DoesNotExist:
        pass
    return redirect('lista_productos')
