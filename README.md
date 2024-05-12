# Comandos

`mkdir nueva_carpeta`
> Crea una carpeta llamada nueva_carpeta

`ls`
> Muestra la lista de archivos

`cd nueva_carpeta`
> Cambia de carpeta

`pwd`
> Muestra la ruta actual

`python -m venv .venv`
> Crea un entorno virtual llamado .venv

`source .venv/bin/activate`
> Activa el entorno virtual en Linux o Mac

`.\venv\Scripts\activate`
> Activa el entorno virtual en Windows

`pip list`
> Muestra la lista de paquetes disponibles en el entorno virtual

`pip install django`
> Instala Django

`django-admin startproject config .`
> Crea un proyecto en el directorio actual

`python manage.py runserver`
> Ejecuta el servidor

`python manage.py startapp app`
> Crea una nueva aplicación llamada app

`python manage.py makemigrations`
> Crea las migraciones, que son archivos Python encargados de la base de datos

`python manage.py migrate`
> Ejecuta las migraciones, para que se realicen los cambios en la base de datos

`python manage.py createsuperuser`
> Crea un usuario administrador para acceder a 127.0.0.1:8000/admin

## Crear archivo de requisitos: requirements.txt

`pip freeze >> requirements.txt`
`pip install -r requirements.txt`
