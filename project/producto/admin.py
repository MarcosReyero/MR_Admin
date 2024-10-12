from django.contrib import admin
from .models import Producto, Categoria
from django.utils.html import format_html

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria', 'mostrar_imagen')

    def mostrar_imagen(self, obj):
        if obj.imagen and hasattr(obj.imagen, 'url'):
            return format_html('<img src="{}" style="width: 50px; height:50px;" />', obj.imagen.url)
        return "Sin imagen"
    mostrar_imagen.short_description = "Imagen"

admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria)
