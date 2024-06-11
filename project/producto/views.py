from django.shortcuts import render, get_object_or_404
from .models import Producto #, Categoria

# Create your views here.


def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/lista_productos.html', {'productos': productos})# def detalle_producto(request, pk):
#     producto = get_object_or_404(Producto, pk=pk)
#     return render(request, 'producto/detalle_producto.html', {'producto': producto})
# 

