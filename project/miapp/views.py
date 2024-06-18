from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.templatetags.static import static
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .forms import PostForm, CommentForm, RegisterForm, UsuarioForm, PerfilUsuarioForm
from .models import Post, Comment, PerfilUsuario
from producto.models import Carrito, Producto  # Asumo que producto.models está correctamente importado
from django.contrib.auth.models import User


@login_required
def home(request):
    return render(request, 'miapp/index.html')


def contact(request):
    context = {
        'linkedin_image_url': static('img/linkedin1.png'),
        'instagram_image_url': static('img/instagram1.png'),
        'gmail_image_url': static('img/gmail3.png')
    }
    return render(request, 'miapp/contact.html', context)


@login_required
def perfil_usuario(request):
    try:
        perfil_usuario_obj = request.user.perfilusuario
    except PerfilUsuario.DoesNotExist:
        perfil_usuario_obj = None

    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST, instance=request.user)
        perfil_form = PerfilUsuarioForm(request.POST, request.FILES, instance=perfil_usuario_obj)
        if usuario_form.is_valid() and perfil_form.is_valid():
            perfil_obj = perfil_form.save(commit=False)
            perfil_obj.user = request.user
            perfil_obj.save()
            usuario_form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('miapp:perfil_usuario')  # Ajustado al namespace si lo tienes así en urls.py
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        usuario_form = UsuarioForm(instance=request.user)
        perfil_form = PerfilUsuarioForm(instance=perfil_usuario_obj)

    return render(request, 'miapp/perfil_usuario.html', {
        'usuario_form': usuario_form,
        'perfil_form': perfil_form,
    })


@login_required
def ver_carrito(request):
    carrito = Carrito.objects.filter(usuario=request.user)
    total = sum(item.producto.precio * item.cantidad for item in carrito)
    return render(request, 'miapp/ver_carrito.html', {'carrito': carrito, 'total': total})


@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user, producto=producto)
    if not created:
        carrito.cantidad += 1
        carrito.save()
    return redirect('producto:detalle_producto', pk=producto_id)


def post_list(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )
    else:
        posts = Post.objects.all()

    context = {
        'posts': posts,
        'query': query,
    }
    return render(request, 'miapp/post_list.html', context)


def about_view(request):
    return render(request, 'miapp/about.html')


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect('miapp:post_detail', pk=post.pk)
        else:
            messages.warning(request, 'Debes estar logeado para comentar en posts. Por favor, inicia sesión o regístrate.')
            return redirect('miapp:login')
    else:
        form = CommentForm()

    return render(request, 'miapp/post_detail.html', {'post': post, 'comments': comments, 'form': form})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('miapp:post_list')
    else:
        form = PostForm()
    return render(request, 'miapp/post_form.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('miapp:post_list')
    return render(request, 'miapp/post_confirm_delete.html', {'post': post})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('miapp:home')
    else:
        form = RegisterForm()
    return render(request, 'miapp/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('miapp:home')
    else:
        form = AuthenticationForm()
    return render(request, 'miapp/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('miapp:home')
