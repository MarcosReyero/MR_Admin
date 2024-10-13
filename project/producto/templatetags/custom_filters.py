from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplica el valor por el argumento."""
    try:
        return value * arg
    except (TypeError, ValueError):
        return ''  # Devuelve vacío si hay un error
