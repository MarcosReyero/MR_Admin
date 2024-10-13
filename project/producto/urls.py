from django.urls import path
from .views import (
    ListaCategoriasView,
    ListaProductosView,
    ListaProductosPorCategoriaView,
    DetalleProductoView,
    AgregarAlCarritoView,
    ActualizarCantidadCarritoView,
    EliminarDelCarritoView,
    VerCarritoView,
    RealizarPedidoView,
     PagosView,
    HistorialPedidosView
)

app_name = 'producto'

urlpatterns = [
    path('', ListaCategoriasView.as_view(), name='lista_categorias'),
    path('productos/', ListaProductosView.as_view(), name='lista_productos'),
    path('categoria/<int:categoria_id>/', ListaProductosPorCategoriaView.as_view(), name='lista_productos_por_categoria'),
    path('producto/<int:pk>/', DetalleProductoView.as_view(), name='detalle_producto'),
    path('producto/<int:producto_id>/agregar/', AgregarAlCarritoView.as_view(), name='agregar_al_carrito'),
    path('carrito/agregar/<int:producto_id>/', AgregarAlCarritoView.as_view(), name='agregar_al_carrito'),
    path('carrito/', VerCarritoView.as_view(), name='ver_carrito'),
    path('carrito/actualizar/<int:carrito_producto_id>/', ActualizarCantidadCarritoView.as_view(), name='actualizar_carrito'),
    path('eliminar-del-carrito/<int:carrito_producto_id>/', EliminarDelCarritoView.as_view(), name='eliminar_del_carrito'),
    path('pedido/realizar/', RealizarPedidoView.as_view(), name='realizar_pedido'),
    path('pagos/', PagosView.as_view(), name='pagos'),
    path('pedido/historial/', HistorialPedidosView.as_view(), name='historial_pedidos'),]
