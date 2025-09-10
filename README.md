# devtalles-django
devTalles Django. Crea aplicaciones web robustas con Python (notas del curso)

Curso original: https://cursos.devtalles.com/courses/take/django/lessons/64692878-variables

# Sección 1: Introducción al curso

[Instalaciones recomendadas](https://gist.github.com/ricardocuellar/76c13654d9c46cf7bcc92abe3ecbe8a6)


# Sección 2: Fundamentos necesarios de Python


### Funciones de orden superior (High Order Function)

```py
def require_auth(func):
    def wrapper(user):
        if user.lower() == "admin":
            return func(user)
        else:
            return "Acceso denegado"

    return wrapper


def admin_dashboard(user):
    return f"Bienvenido al panel, {user}"


auth_view_dashboard = require_auth(admin_dashboard)

print(auth_view_dashboard("Admin"))
print(auth_view_dashboard("Invitado"))
```

### Decoradores

```py
def require_auth(func):
    def wrapper(user):
        if user.lower() == "admin":
            return func(user)
        else:
            return "Acceso denegado"

    return wrapper

# auth_view_dashboard = require_auth(admin_dashboard)
# print(auth_view_dashboard("Admin"))

@require_auth
def admin_dashboard(user):
    return f"Bienvenido al panel, {user}"

print(admin_dashboard("Admin"))
print(admin_dashboard("ADMIN"))
```

# Sección 3. Introducción a Django 

En django se usa el modelo MTV y en el mismo donde, en relación al modelo MVC, la vista es el controlador y el template es la vista, más el modelo que es igual. En este modelo el controlador es el encargado de manejar la lógica de la aplicación, interactuar con el modelo y seleccionar la plantilla adecuada para renderizar la respuesta.

### Instalar django de forma global

```sh
python3 -m pip install Django
```

### Crear entorno virtual e instalar django

```sh
python3 - m venv venv
source venv/bin/activate
pip install django

pip freeze > requirements.txt
cat requirements.txt

# Crear projecto myproject
django-admin startproject myproject
```

El archivo `asgi.py` en Django sirve como punto de entrada para aplicaciones ASGI (Asynchronous Server Gateway Interface), por ejemplo: HTTP requests síncronos y asíncronos, WebSocket (chat, push notifications), Conexiones de larga duración y Protocolos en tiempo real.

WSGI `wsgi.py` es el estándar de Python para comunicación entre servidores web y aplicaciones web. Es el protocolo síncrono tradicional que Django ha usado desde sus inicios. Por ejemplo: interfaz de servidores web (conecta django con servidores apache, nginx, gunicorn), manejo de requests HTTP síncronos (tradicionales). 


### Ejecutar django

```sh
python3 manage.py runserver

open http://127.0.0.1:8000/
```

### Crear una aplicación

*En el mundo de django las aplicaciones con paquetes o módulos*

```sh
python3 manage.py startapp <app-name>

python3 manage.py runserver
```

### Registrar la aplicación

```py
# myproject/settings.py
INSTALLED_APPS = [
    ...
    'myapp',
]
```

### Crear una vista

```py
# myapp/views.py
from django.http import HttpResponse

def home(request):
    return HttpResponse("¡Hola, mundo!")            
```

### Mapear la vista a una URL

```py
# myapp/urls.py
from django.urls import path
from .views import home

urlpatterns = [
    path('', home, name='home'),
]
```

```py
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]
```     

Las views manejan la lógica de la aplicación, interactúan con el modelo y seleccionan la plantilla adecuada para renderizar la respuesta. Las views reciben solicitudes HTTP, procesan los datos necesarios y devuelven respuestas HTTP, estas pueden funcionar usando `funciones` o `clases`.

La función `reverse` se utiliza para obtener la URL correspondiente a una vista basada en su nombre. Esto es útil para evitar hardcoding de URLs en las plantillas y vistas, facilitando el mantenimiento y la refactorización del código.

### Crear una plantilla

_Es una buena práctica crear una carpeta llamada `templates` dentro de la aplicación, y a su vez crear una subcarpeta con el nombre de la aplicación dentro de `templates`._

```html
<!-- myapp/templates/myapp/home.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
</head>
<body>
    <h1>Welcome to the Home Page</h1>
</body>
</html> 
```

```py
# myapp/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'myapp/home.html')           
```
### Configurar las plantillas en settings.py

```py
INSTALLED_APPS = [
    ...
    'myapp',
]   
TEMPLATES = [
    {
        ...
        'DIRS': [],
        'APP_DIRS': True, # Busca plantillas en las carpetas 'templates' de cada app
        ...
    },
]
```

# Filtros y etiquetas en plantillas

Ejemplos:

```html
<p>Nombre en mayúsculas: {{ name | upper }}</p>
<p>Nombre capitalizado: {{ name | title }}</p>
<p>Nombre en minúsculas: {{ name | lower }}</p>
<p>Edad en 5 años: {{ age | add:5 }}</p>
<p>Fecha actual: {{ current_date | date:"F j, Y" }}</p>
<p>Lista de items:</p>
<ul>
    {% for item in items %}
        <li>{{ item }}</li>
    {% empty %}
        <li>No hay items disponibles.</li>
    {% endfor %}
</ul>
<p>Condicional:</p>
{% if user.is_authenticated %}
    <p>Bienvenido, {{ user.username }}!</p>
{% else %}
    <p>Por favor, inicia sesión.</p>
{% endif %}
```
