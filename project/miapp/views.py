from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    return render(request, 'miapp/index.html')

def contact(request):
    return render(request, 'miapp/contact.html')

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'miapp/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user  # Asignar el autor como el usuario logeado
                comment.save()
                return redirect('miapp:post_detail', pk=post.pk)
        else:
            messages.warning(request, 'Debes estar logeado para comentar en posts. Por favor, inicia sesión o regístrate.')
            return redirect('miapp:login')
    else:
        form = CommentForm()

    return render(request, 'miapp/post_detail.html', {'post': post, 'comments': comments, 'form': form})    

@login_required(login_url='miapp:login')
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('miapp:post_list')
    else:
        form = PostForm()
    return render(request, 'miapp/post_form.html', {'form': form})

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

def user_logout(request):
    logout(request)
    return redirect('miapp:home')
