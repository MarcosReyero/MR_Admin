# Tipos de Datos en Django

## Cadenas

- `CharField`: Un campo de texto corto con una longitud máxima fija. Se especifica mediante el parámetro `max_length`. El valor predeterminado de `max_length` es 255 caracteres. Es importante tener en cuenta que la longitud máxima de un campo `CharField` depende de la base de datos subyacente utilizada. Por ejemplo, en MySQL, el límite máximo es de 65.535 caracteres. En PostgreSQL, el límite máximo es de 1.073.741.823 caracteres.

- `TextField`: Un campo de texto largo sin longitud máxima. Es limitada por la capacidad de almacenamiento de la base de datos subyacente.

## Números

- `IntegerField`: Un campo que almacena números enteros (desde -2147483648 hasta 2147483647. SQLite soporta un rango más pequeño)

- `BigIntegerField`: Un campo que almacena números enteros muy grandes (desde -9223372036854775808 hasta 9223372036854775807. SQLite no lo soporta).

- `DecimalField`: Un campo que almacena números decimales precisos. Python no tiene un límite absoluto en su rango de valores, pero la capacidad de la base de datos subyacente para almacenar valores decimales puede estar limitada. Almacena los valores numéricos como decimales precisos, lo que significa que puede almacenar números con una precisión fija y escala variable, lo que es útil para aplicaciones financieras y otras que requieren precisión decimal.

- `FloatField`: Un campo que almacena números en coma flotante (rango de aproximadamente 2.23 × 10^-308 hasta 1.80 × 10^308). Si la precisión decimal no es crítica, o si se requiere una precisión muy alta en valores numéricos muy grandes o muy pequeños, `FloatField` podría ser más adecuado.

- `PositiveIntegerField`: Un campo que almacena números enteros positivos. Rango de 0 a 2.147.483.647.

- `PositiveSmallIntegerField`: Un campo que almacena números enteros pequeños y positivos. Rango de 0 a 32.767.

- `SmallIntegerField`: Un campo que almacena números enteros pequeños. Rango de -32.768 a 32.767

## Fechas y horas

- `DateField`: Un campo que almacena una fecha.

- `DateTimeField`: Un campo que almacena una fecha y hora.

- `TimeField`: Un campo que almacena una hora.

- `DurationField`: Un campo que almacena un período de tiempo.

## Propias de las relaciones entre modelos

- `AutoField`: Un campo que almacena un número de identificación único generado automáticamente por Django. `AutoField` se utiliza para crear un campo de clave primaria único para el modelo que lo contiene. El valor del campo `AutoField` se genera automáticamente por la base de datos, sin que el usuario tenga que especificarlo. Al igual que con `BigIntegerField`, el valor máximo que puede ser almacenado en un `AutoField` depende del tipo de base de datos utilizado. En la mayoría de las bases de datos, incluyendo MySQL y PostgreSQL, el valor máximo que puede ser almacenado en un `AutoField` es 2147483647 (2^31 - 1) para campos `AutoField` de tipo `IntegerField`, y 9223372036854775807 (2^63 - 1) para campos `AutoField` de tipo `BigAutoField`.

- `ForeignKey`: Un campo que establece una relación entre dos modelos. Este campo almacena la clave principal de un modelo relacionado.

- `ManyToManyField`: Un campo que establece una relación muchos a muchos entre dos modelos. Este campo almacena una tabla intermedia que vincula las dos tablas relacionadas.

- `UUIDField`: Un campo que almacena un identificador único universal (`UUID`). Un `UUID` es un identificador único que consta de 32 caracteres hexadecimales, divididos en cinco grupos separados por guiones. Un `UUID` se puede utilizar como un identificador único para cualquier cosa, como usuarios, publicaciones de blog, imágenes, etc.

Hay varias razones por las que se puede utilizar un `UUIDField` en lugar de un `IntegerField` o `AutoField` convencionales:

Universalidad: Un `UUID` es un identificador globalmente único que se puede generar en cualquier sistema o máquina sin preocuparse por colisiones de claves primarias en la base de datos.

Privacidad: A diferencia de los identificadores incrementales (`IntegerField` o `AutoField`), no permiten adivinar la existencia de otros objetos en la base de datos.

Escalabilidad: Cuando se trabaja con bases de datos distribuidas, generar un `AutoField` convencional puede ser un cuello de botella para la escalabilidad. Los `UUIDField` pueden ser generados de forma independiente en cada nodo de la base de datos distribuida sin conflictos.

Sencillez: El campo `UUIDField` es muy fácil de usar en comparación con la complejidad de la generación de claves primarias únicas y escalables en bases de datos distribuidas.

En general, `UUIDField` es útil para aplicaciones web que requieren un identificador único y global para objetos en la base de datos.

## `on_delete` en `ForeignKey`

El parámetro `on_delete` es propio de `ForeignKey` . Acepta los siguientes valores:

- `CASCADE`: Borra los objetos relacionados cuando se borra el objeto principal.
- `PROTECT`: Evita la eliminación del objeto principal si hay objetos relacionados. Genera una excepción `ProtectedError`
- `SET_NULL`: Establece los campos relacionados en `NULL` cuando se borra el objeto principal. Esta opción solo se puede usar en campos que permiten valores nulos (`null=True`).
- `SET_DEFAULT`: Establece los campos relacionados en su valor predeterminado cuando se borra el objeto principal. Esta opción solo se puede usar en campos que tienen un valor predeterminado.
- `SET()`: Establece los campos relacionados en un valor especificado cuando se borra el objeto principal. El valor se especifica utilizando un objeto de modelo o un valor constante.
- `DO_NOTHING`: No hace nada cuando se borra el objeto principal. Esto puede resultar en referencias rotas en la base de datos y debe usarse con precaución.

Es importante tener en cuenta que algunos tipos de `on_delete` pueden no ser compatibles con ciertos motores de base de datos. Por ejemplo, `SET_DEFAULT` no está disponible en SQLite. Además, se debe tener cuidado al utilizar `SET_NULL` , ya que puede introducir referencias rotas en la base de datos y afectar la integridad de los datos.

## Archivos

- `FileField`: se utiliza para almacenar archivos en el sistema de archivos del servidor. Puede almacenar cualquier tipo de archivo, incluyendo imágenes, documentos, audio, video, etc. Cuando se carga un archivo en un campo `FileField`, Django guarda el archivo en una ubicación determinada del sistema de archivos y almacena la ruta de archivo en la base de datos. Un campo `FileField` puede ser útil para almacenar archivos grandes o para permitir que los usuarios suban archivos a través de un formulario en el sitio web.

- `ImageField`: es una subclase de `FileField` y se utiliza específicamente para almacenar imágenes en el sistema de archivos del servidor. Al igual que `FileField`, `ImageField` guarda el archivo de imagen en una ubicación determinada del sistema de archivos y almacena la ruta de archivo en la base de datos. Además, `ImageField` realiza algunas validaciones adicionales para garantizar que el archivo cargado sea una imagen válida y puede realizar algunas transformaciones en la imagen cargada, como cambiar su tamaño o formato. Un campo `ImageField` puede ser útil para aplicaciones web que requieren la carga y manipulación de imágenes.

- `BinaryField`: se utiliza para almacenar datos binarios arbitrarios, como archivos PDF, archivos ZIP, o cualquier otro tipo de archivo que no sea una imagen o un archivo de texto. Un campo `BinaryField` almacena los datos binarios directamente en la base de datos en lugar de guardar el archivo en el sistema de archivos del servidor. Un campo `BinaryField` puede ser útil para almacenar archivos pequeños o para aplicaciones que requieren el almacenamiento de datos binarios directamente en la base de datos.

## Otros tipos de campo

- `BooleanField`: Un campo que almacena valores booleanos (True o False).
- `EmailField`: Un campo que almacena una dirección de correo electrónico. Formato: El campo `EmailField` verifica que el valor ingresado en el campo tenga un formato de dirección de correo electrónico válido, es decir, que contenga un nombre de usuario, una arroba (@) y un nombre de dominio.

Longitud: El campo `EmailField` verifica que la longitud total del correo electrónico no exceda los límites permitidos en la base de datos.

Dominio: El campo `EmailField` verifica que el nombre de dominio del correo electrónico tenga un formato válido y exista un registro DNS correspondiente al dominio.

Caracteres válidos: El campo `EmailField` verifica que los caracteres utilizados en el correo electrónico estén permitidos según las normas RFC.

Unicidad: En algunos casos, el campo `EmailField` también puede verificar que la dirección de correo electrónico no esté ya registrada en la base de datos, para garantizar la unicidad.

- `URLField`: Un campo que almacena una URL. Formato: El campo `URLField` verifica que el valor ingresado en el campo tenga un formato de URL válido, es decir, que comience con un esquema (como "http://" o "https://"), seguido de un nombre de dominio y una ruta.

Longitud: El campo `URLField` verifica que la longitud total de la URL no exceda los límites permitidos en la base de datos.

Dominio: El campo `URLField` verifica que el nombre de dominio de la URL tenga un formato válido y exista un registro DNS correspondiente al dominio.

Protocolo: El campo `URLField` verifica que el esquema de la URL esté permitido según las normas RFC.

Caracteres válidos: El campo `URLField` verifica que los caracteres utilizados en la URL estén permitidos según las normas RFC.

Unicidad: En algunos casos, el campo `URLField` también puede verificar que la URL no esté ya registrada en la base de datos, para garantizar la unicidad.

- `SlugField`: Un campo que almacena una cadena corta y legible para humanos, utilizada en las URL. Algunas de las validaciones que realiza el campo `SlugField` son las siguientes:

Caracteres válidos: El campo `SlugField` verifica que la cadena de texto ingresada solo contenga caracteres válidos para un identificador de URL. Estos caracteres pueden incluir letras en minúsculas, números y guiones medios ("-"), pero no pueden contener espacios, mayúsculas ni otros caracteres especiales.

Unicidad: El campo `SlugField` puede verificar que el valor ingresado sea único en la base de datos. Si el campo se configura con el parámetro `unique=True`, Django generará un error si se intenta guardar un valor de slug que ya existe en la base de datos.

Longitud máxima: El campo `SlugField` también puede limitar la longitud máxima del valor de `slug` que se almacena en la base de datos.

Formato: El campo `SlugField` puede verificar que la cadena de texto ingresada tenga un formato válido como `slug`. En general, esto implica asegurarse de que la cadena no comience ni termine con un guion medio, y que no haya dos guiones medios consecutivos.

- `JSONField`: Un campo que almacena datos en formato JSON. Las validaciones que se realizan en el campo `JSONField` son las siguientes:

Sintaxis JSON válida: El campo `JSONField` verifica que los datos ingresados en el campo tengan una sintaxis JSON válida. Si los datos no cumplen con las reglas de sintaxis JSON, se generará un error.

Tipos de datos permitidos: El campo `JSONField` verifica que los datos ingresados tengan los tipos de datos permitidos según las especificaciones JSON. Por ejemplo, los datos pueden ser objetos JSON, matrices JSON, cadenas de caracteres JSON, números JSON, valores booleanos JSON (`true` o `false`) o el valor `null` JSON.

Longitud máxima: El campo `JSONField` también puede limitar la longitud máxima de los datos JSON que se almacenan en la base de datos.

- `ArrayField`: Un campo que almacena una matriz de valores, compatible con PostgreSQL. Se utiliza para almacenar una lista de valores de un determinado tipo en una sola columna de una base de datos relacional. Cuando se utiliza este campo, se realizan algunas validaciones automáticas en los datos antes de ser almacenados en la base de datos.

Las validaciones que se realizan en el campo `ArrayField` son las siguientes:

Tipo de datos: El campo `ArrayField` verifica que los datos ingresados en la lista sean del tipo de datos especificado en la definición del campo. Por ejemplo, si el campo `ArrayField` está definido como `ArrayField(models.IntegerField())`, se asegurará de que todos los valores en la lista sean de tipo `int`.

Longitud mínima y máxima: El campo `ArrayField` puede limitar la longitud mínima y máxima de la lista. Si se intenta guardar una lista con una longitud menor que la mínima o mayor que la máxima, se generará un error.

Valores únicos: El campo `ArrayField` también puede verificar que todos los valores en la lista sean únicos. Si se intenta guardar una lista con valores duplicados, se generará un error.

Valores válidos: El campo `ArrayField` puede verificar que todos los valores en la lista cumplan con ciertas condiciones. Por ejemplo, si el campo `ArrayField` está definido como `ArrayField`(`models.CharField(max_length=50)`), se asegurará de que cada valor en la lista sea una cadena de caracteres de longitud máxima 50.

- `IPAddressField`: Un campo que almacena una dirección IP.

- `GenericIPAddressField`: Un campo que almacena una dirección IP genérica (IPv4 o IPv6).

[Volver](../README.md)
