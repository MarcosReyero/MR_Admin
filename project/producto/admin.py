from django.contrib import admin
from .models import Categoria, Producto, Carrito, CarritoProducto, Orden, OrdenProducto
from django.utils.html import format_html

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria', 'mostrar_imagen')

    def mostrar_imagen(self, obj):
        if obj.imagen and hasattr(obj.imagen, 'url'):
            return format_html('<img src="{}" style="width: 50px; height:50px;" />', obj.imagen.url)
        return "Sin imagen"
    mostrar_imagen.short_description = "Imagen"



@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha_agregado')
    search_fields = ('usuario__username',)

@admin.register(CarritoProducto)
class CarritoProductoAdmin(admin.ModelAdmin):
    list_display = ('carrito', 'producto', 'cantidad')
    search_fields = ('carrito__usuario__username', 'producto__nombre')

@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha', 'total', 'pagado')
    search_fields = ('usuario__username',)
    list_filter = ('pagado', 'fecha')

@admin.register(OrdenProducto)
class OrdenProductoAdmin(admin.ModelAdmin):
    list_display = ('orden', 'producto', 'cantidad', 'precio')
    search_fields = ('orden__usuario__username', 'producto__nombre')