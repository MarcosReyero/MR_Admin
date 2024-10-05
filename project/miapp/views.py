from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.templatetags.static import static
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy
from .forms import PostForm, CommentForm, RegisterForm, UsuarioForm, PerfilUsuarioForm
from .models import Post, Comment, PerfilUsuario
from producto.models import Carrito, Producto
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages

class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'miapp/index.html')

class ContactView(View):
    def get(self, request):
        return render(request, 'miapp/contact.html')

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        template = render_to_string('email-template.html', {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message
        })

        email_sender = EmailMessage(
            subject,
            template,
            'MR-ADMIN <' + settings.EMAIL_HOST_USER + '>',  # Aquí especificas el nombre que aparecerá como remitente
            ['reyeromateo@gmail.com']
        )
        email_sender.content_subtype = 'html'
        email_sender.fail_silently = False

        try:
            email_sender.send()
            messages.success(request, 'El correo electrónico se envió correctamente')
        except Exception as e:
            messages.error(request, f'Ocurrió un error al enviar el correo: {str(e)}')

        return redirect('miapp:contact')           
class PerfilUsuarioView(LoginRequiredMixin, View):
    def get(self, request):
        perfil_usuario_obj = getattr(request.user, 'perfilusuario', None)
        usuario_form = UsuarioForm(instance=request.user)
        perfil_form = PerfilUsuarioForm(instance=perfil_usuario_obj)
        return render(request, 'miapp/perfil_usuario.html', {
            'usuario_form': usuario_form,
            'perfil_form': perfil_form,
        })

    def post(self, request):
        perfil_usuario_obj = getattr(request.user, 'perfilusuario', None)
        usuario_form = UsuarioForm(request.POST, instance=request.user)
        perfil_form = PerfilUsuarioForm(request.POST, request.FILES, instance=perfil_usuario_obj)

        if usuario_form.is_valid() and perfil_form.is_valid():
            usuario_form.save()  # Actualiza el usuario
            perfil_form.save()   # Actualiza el perfil
            return redirect('miapp:perfil_usuario')  # Redirigir a la misma página o donde prefieras

        return render(request, 'miapp/perfil_usuario.html', {
            'usuario_form': usuario_form,
            'perfil_form': perfil_form,
        })    
        
        def post(self, request):

            perfil_usuario_obj = getattr(request.user, 'perfilusuario', None)
            usuario_form = UsuarioForm(request.POST, instance=request.user)
            perfil_form = PerfilUsuarioForm(request.POST, request.FILES, instance=perfil_usuario_obj)
            
            if usuario_form.is_valid() and perfil_form.is_valid():
                perfil_obj = perfil_form.save(commit=False)
                perfil_obj.user = request.user
                perfil_obj.save()
                usuario_form.save()
                messages.success(request, 'Perfil actualizado correctamente.')
                return redirect('miapp:perfil_usuario')
            else:
                messages.error(request, 'Por favor, corrige los errores en el formulario.')
                return render(request, 'miapp/perfil_usuario.html', {
                    'usuario_form': usuario_form,
                    'perfil_form': perfil_form,
            })
class PostListView(View):
    def get(self, request):
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

class AboutView(View):
    def get(self, request):
        return render(request, 'miapp/about.html')

class PostDetailView(DetailView):
    model = Post
    template_name = 'miapp/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object)
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = self.object
                comment.author = request.user
                comment.save()
                return redirect('miapp:post_detail', pk=self.object.pk)
        else:
            messages.warning(request, 'Debes estar logeado para comentar en posts.')
            return redirect('miapp:login')

class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'miapp/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('miapp:post_list')

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'miapp/post_confirm_delete.html'

    def get_success_url(self):
        return reverse('miapp:post_list')

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'miapp/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('miapp:home')
        return render(request, 'miapp/register.html', {'form': form})

class UserLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'miapp/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('miapp:home')
        return render(request, 'miapp/login.html', {'form': form})

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('miapp:home')


