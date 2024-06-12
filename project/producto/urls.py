from django.urls import path
from . import views

app_name = 'producto'

urlpatterns = [
    path('', views.lista_categorias, name='lista_categorias'),
    path('categoria/<int:categoria_id>/', views.lista_productos_por_categoria, name='lista_productos_por_categoria'),
    path('producto/<int:pk>/', views.detalle_producto, name='detalle_producto'),  # Agregado para detalles del producto
]
