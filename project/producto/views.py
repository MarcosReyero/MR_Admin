from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Categoria, Carrito, Orden, OrdenProducto
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

class ListaCategoriasView(View):
    def get(self, request):
        categorias = Categoria.objects.all()
        return render(request, 'productos/lista_categorias.html', {'categorias': categorias})

class ListaProductosView(View):
    def get(self, request):
        productos = Producto.objects.all()
        return render(request, 'productos/lista_productos.html', {'productos': productos, 'categoria': None})

class ListaProductosPorCategoriaView(View):
    def get(self, request, categoria_id=None):
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

class DetalleProductoView(View):
    def get(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        return render(request, 'productos/detalle_producto.html', {'producto': producto})

class AgregarAlCarritoView(LoginRequiredMixin, View):
    def post(self, request, producto_id):
        producto = get_object_or_404(Producto, id=producto_id)
        carrito, created = Carrito.objects.get_or_create(usuario=request.user, producto=producto)

        if not created:
            carrito.cantidad += 1
            carrito.save()

        return redirect('producto:detalle_producto', pk=producto_id)

class VerCarritoView(LoginRequiredMixin, View):
    def get(self, request):
        carrito = Carrito.objects.filter(usuario=request.user)
        total = sum(item.producto.precio * item.cantidad for item in carrito)
        return render(request, 'miapp/ver_carrito.html', {'carrito': carrito, 'total': total})

class RealizarPedidoView(LoginRequiredMixin, View):
    def post(self, request):
        carrito = Carrito.objects.filter(usuario=request.user)
        if not carrito:
            return redirect('producto:lista_productos')
        
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
        return redirect('producto:historial_pedidos')

class HistorialPedidosView(LoginRequiredMixin, View):
    def get(self, request):
        ordenes = Orden.objects.filter(usuario=request.user)
        return render(request, 'productos/historial_pedidos.html', {'ordenes': ordenes})
