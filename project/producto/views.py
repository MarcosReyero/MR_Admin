from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria

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
