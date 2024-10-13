from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Producto, Categoria, Carrito, Orden, OrdenProducto, CarritoProducto, Orden
from django.contrib import messages


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
            'hay_productos': productos.exists(),
        }
        return render(request, 'productos/lista_productos.html', context)

class DetalleProductoView(View):
    def get(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        return render(request, 'productos/detalle_producto.html', {'producto': producto})

class AgregarAlCarritoView(LoginRequiredMixin, View):
    def post(self, request, producto_id):
        producto = get_object_or_404(Producto, id=producto_id)
        cantidad = int(request.POST.get('cantidad', 1))
        
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)

        carrito_producto, created = CarritoProducto.objects.get_or_create(carrito=carrito, producto=producto)

        if not created:
            carrito_producto.cantidad += cantidad  
        else:
            carrito_producto.cantidad = cantidad  

        carrito_producto.save()  

        return redirect('producto:detalle_producto', pk=producto_id)

class VerCarritoView(View):
    def get(self, request):
        if request.user.is_authenticated:
            carrito = get_object_or_404(Carrito, usuario=request.user)
            carrito_productos = CarritoProducto.objects.filter(carrito=carrito)

            # Debugging: Imprimir productos en el carrito
            print(carrito_productos.count())  # Esto debería mostrar cuántos productos hay

            total_carrito = carrito.total()  # Asegúrate de que total() esté definido correctamente

            return render(request, 'productos/ver_carrito.html', {
                'carrito_productos': carrito_productos,
                'total': total_carrito,
            })
        else:
            return redirect('miapp:login')
        
        
class ActualizarCantidadCarritoView(LoginRequiredMixin, View):
    def post(self, request, carrito_producto_id):
        carrito_producto = get_object_or_404(CarritoProducto, id=carrito_producto_id)
        nueva_cantidad = request.POST.get('cantidad')
        
        try:
            nueva_cantidad = int(nueva_cantidad)  # Intenta convertir a entero
            if nueva_cantidad > 0:
                carrito_producto.cantidad = nueva_cantidad
                carrito_producto.save()
            else:
                messages.error(request, "La cantidad debe ser mayor que cero.")
        except (ValueError, TypeError):  # Captura errores de conversión
            messages.error(request, "Por favor, introduce un número válido para la cantidad.")
        
        return redirect('producto:ver_carrito')

class EliminarDelCarritoView(LoginRequiredMixin, View):
    def post(self, request, carrito_producto_id):  # Cambié carrito_id por carrito_producto_id
        carrito_producto = get_object_or_404(CarritoProducto, id=carrito_producto_id)
        carrito_producto.delete()  # Elimina solo el producto del carrito
        return redirect('producto:ver_carrito')


class RealizarPedidoView(LoginRequiredMixin, View):
    def post(self, request):
        carrito = get_object_or_404(Carrito, usuario=request.user)
        carrito_productos = CarritoProducto.objects.filter(carrito=carrito)

        if not carrito_productos.exists():
            return redirect('producto:lista_productos')

        total = sum(item.producto.precio * item.cantidad for item in carrito_productos)

        if total > 0:
            orden = Orden.objects.create(usuario=request.user, total=total, pagado=False)
            for item in carrito_productos:
                OrdenProducto.objects.create(
                    orden=orden,
                    producto=item.producto,
                    cantidad=item.cantidad,
                    precio=item.producto.precio
                )
            carrito_productos.delete()

            messages.success(request, "Tu pedido se ha realizado con éxito.")
            return redirect('producto:pagos')
        
        return redirect('producto:lista_productos')
    
class HistorialPedidosView(LoginRequiredMixin, View):
    def get(self, request):
        ordenes = Orden.objects.filter(usuario=request.user).order_by('-fecha')
        return render(request, 'productos/historial_pedidos.html', {'ordenes': ordenes})



class PagosView(LoginRequiredMixin, View):
    def get(self, request):
        ordenes = Orden.objects.filter(usuario=request.user, pagado=False)

        if not ordenes.exists():
            return redirect('producto:carrito')

        # Tomar la última orden no pagada
        orden = ordenes.last()

        return render(request, 'productos/components/pagos.html', {'orden': orden})

    def post(self, request):
        orden_id = request.POST.get('orden_id')
        orden = get_object_or_404(Orden, id=orden_id, usuario=request.user, pagado=False)

        orden.pagado = True
        orden.save()

        return redirect('producto:historial_pedidos')