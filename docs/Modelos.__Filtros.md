# `Filter`

- Igualdad: `campo="valor"`
    > Filtra los objetos donde el campo sea igual al valor proporcionado.

- Desigualdad: `campo__ne="valor"`
    > Filtra los objetos donde el campo no sea igual al valor proporcionado.

## Comparación

- Mayor que: `campo__gt=valor`
    > Filtra los objetos donde el campo sea mayor que el valor proporcionado.

- Mayor o igual que: `campo__gte=valor`
    > Filtra los objetos donde el campo sea mayor o igual que el valor proporcionado.

- Menor que: `campo__lt=valor`
    > Filtra los objetos donde el campo sea menor que el valor proporcionado.

- Menor o igual que: `campo__lte=valor`
    > Filtra los objetos donde el campo sea menor o igual que el valor proporcionado.

## Búsqueda en cadenas de texto

- Contiene: `campo__contains="valor"`
    > Filtra los objetos donde el campo contenga el valor proporcionado.

- Comienza con: `campo__startswith="valor"`
    > Filtra los objetos donde el campo comience con el valor proporcionado.

- Termina con: campo`__endswith`="valor"
    > Filtra los objetos donde el campo termine con el valor proporcionado.

## Expresiones regulares: `campo__regex="patrón"`

Filtra los objetos donde el campo coincida con el patrón de expresión regular proporcionado.

## Consultas lógicas

- `AND`: `Q(condición1) & Q(condición2)`
    > Combina condiciones utilizando el operador lógico `AND`
- `OR`: `Q(condición1) | Q(condición2)`
    > Combina condiciones utilizando el operador lógico `OR`
- `NOT`: `~Q(condición)`
    > Niega una condición.

## Campos relacionados

- Filtrado a través de una relación
    > `campo_relacionado__campo="valor"`
    Filtra los objetos basados en el valor de un campo relacionado.

## Nota

`filter()` Devuelve un objeto `QuerySet` que puede ser iterado y utilizado en otras operaciones, como ordenamiento, agregación y más.

