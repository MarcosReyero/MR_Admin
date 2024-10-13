from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    destacado = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.nombre} {'(Destacado)' if self.destacado else ''}"    
class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)  
    productos = models.ManyToManyField(Producto, through='CarritoProducto')
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

    def __iter__(self):
        for carrito_producto in self.carritaproducto_set.all():
            yield carrito_producto

    def total(self):
        return sum(item.producto.precio * item.cantidad for item in self.carrito_productos.all())

class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='carrito_productos')  # Agregar related_name
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en el carrito"
class Orden(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    pagado = models.BooleanField(default=False)

    def __str__(self):
        return f"Orden {self.id} de {self.usuario.username}"

class OrdenProducto(models.Model):
    orden = models.ForeignKey(Orden, related_name='productos', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"