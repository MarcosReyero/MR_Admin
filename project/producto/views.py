from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria

def lista_categorias(request):
    print("Vista lista_categorias llamada")
    categorias = Categoria.objects.all()
    print(f"Categorías: {categorias}")  # Añadido para depuración
    return render(request, 'productos/lista_categorias.html', {'categorias': categorias})

def lista_productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria)
    return render(request, 'productos/lista_productos_por_categoria.html', {'productos': productos, 'categoria': categoria})

def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/detalle_producto.html', {'producto': producto})

