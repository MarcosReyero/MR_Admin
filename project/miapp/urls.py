from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    HomeView,
    AboutView,
    ContactView,
    PerfilUsuarioView,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostDeleteView,
    RegisterView,
    UserLoginView,
    UserLogoutView,
)

app_name = 'miapp'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('login/', auth_views.LoginView.as_view(template_name='miapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('perfil/', PerfilUsuarioView.as_view(), name='perfil_usuario'),
]
