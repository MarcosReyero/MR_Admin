from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import perfil_usuario, ver_carrito
from .views import home, contact, perfil_usuario, ver_carrito, agregar_al_carrito, post_list, post_detail, post_create, post_delete, register, user_login, user_logout, about_view




app_name = 'miapp'

#urlpatterns = [
#    path('', views.home, name='home'),  # Ruta principal
#    path('posts/', views.post_list, name='post_list'),  # Lista de posts
#    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # Detalle de un post
#    path('post/new/', views.post_create, name='post_create'),  # Crear un nuevo post
#    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),  # Eliminar un post
#    path('contact/', views.contact, name='contact'),
#    path('register/', views.register, name='register'),
#    path('login/', views.user_login, name='login'), 
#    path('logout/', views.user_logout, name='logout'), # Página de contacto
#    # Otras rutas de URL aquí
#]
app_name = 'miapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact, name='contact'),
    path('posts/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('login/', auth_views.LoginView.as_view(template_name='miapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('perfil/', perfil_usuario, name='perfil_usuario'),
    path('carrito/', ver_carrito, name='ver_carrito'),
]
