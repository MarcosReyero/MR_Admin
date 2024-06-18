from django.shortcuts import render,redirect, get_object_or_404
from .models import Producto, Categoria, Carrito,Orden, OrdenProducto
from django.contrib.auth.decorators import login_required


def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'productos/lista_categorias.html', {'categorias': categorias})

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/lista_productos.html', {'productos': productos, 'categoria': None})

def lista_productos_por_categoria(request, categoria_id=None):
    categoria = None
    productos = Producto.objects.all()
    if categoria_id:
        categoria = get_object_or_404(Categoria, id=categoria_id)
        productos = productos.filter(categoria=categoria)

    context = {
        'categoria': categoria,
        'productos': productos,
    }
    return render(request, 'productos/lista_productos.html', context)
def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/detalle_producto.html', {'producto': producto})

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        carrito, created = Carrito.objects.get_or_create(
            usuario=request.user,
            producto=producto,
        )
        if not created:
            carrito.cantidad += cantidad
        carrito.save()
        return redirect('detalle_producto', pk=producto_id)
    return redirect('detalle_producto', pk=producto_id)

@login_required
def ver_carrito(request):
    carrito = Carrito.objects.filter(usuario=request.user)
    total = sum(item.producto.precio * item.cantidad for item in carrito)
    return render(request, 'productos/ver_carrito.html', {'carrito': carrito, 'total': total})

@login_required
def realizar_pedido(request):
    carrito = Carrito.objects.filter(usuario=request.user)
    if not carrito:
        return redirect('lista_productos')
    
    total = sum(item.producto.precio * item.cantidad for item in carrito)
    orden = Orden.objects.create(usuario=request.user, total=total, pagado=False)
    for item in carrito:
        OrdenProducto.objects.create(
            orden=orden,
            producto=item.producto,
            cantidad=item.cantidad,
            precio=item.producto.precio
        )
    carrito.delete()
    return redirect('historial_pedidos')

@login_required
def historial_pedidos(request):
    ordenes = Orden.objects.filter(usuario=request.user)
    return render(request, 'productos/historial_pedidos.html', {'ordenes': ordenes})