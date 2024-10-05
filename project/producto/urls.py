from django.urls import path
from .views import (
    ListaCategoriasView,
    ListaProductosView,
    ListaProductosPorCategoriaView,
    DetalleProductoView,
    AgregarAlCarritoView,
    VerCarritoView,
    RealizarPedidoView,
    HistorialPedidosView
)

app_name = 'producto'

urlpatterns = [
    path('', ListaCategoriasView.as_view(), name='lista_categorias'),
    path('productos/', ListaProductosView.as_view(), name='lista_productos'),
    path('categoria/<int:categoria_id>/', ListaProductosPorCategoriaView.as_view(), name='lista_productos_por_categoria'),
    path('producto/<int:pk>/', DetalleProductoView.as_view(), name='detalle_producto'),
    path('producto/<int:producto_id>/agregar/', AgregarAlCarritoView.as_view(), name='agregar_al_carrito'),
    path('carrito/', VerCarritoView.as_view(), name='ver_carrito'),  # Agrega la vista para ver el carrito
    path('realizar-pedido/', RealizarPedidoView.as_view(), name='realizar_pedido'),  # Agrega la vista para realizar un pedido
    path('historial-pedidos/', HistorialPedidosView.as_view(), name='historial_pedidos'),  # Agrega la vista para el historial de pedidos
]
