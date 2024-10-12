from django import forms
from .models import Post, Comment
from .models import PerfilUsuario


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', ]
            ext = os.path.splitext(image.name)[1]
            if ext.lower() not in valid_extensions:
                raise ValidationError("El formato de imagen no es válido. Solo se permiten: JPG, JPEG, PNG, WEBP Y GIF.")
        return image        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [ 'body']


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['foto_perfil']

    def clean_foto_perfil(self):
        foto = self.cleaned_data.get('foto_perfil')
        if foto:
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            ext = os.path.splitext(foto.name)[1]
            if ext.lower() not in valid_extensions:
                raise ValidationError("El formato de imagen no es válido. Solo se permiten: JPG, JPEG, PNG, WEBP Y GIF.")
        return foto